from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)



def get_forecast_data():

    forecast_df = pd.read_csv(
        "results/forecast_results.csv"
    )

    forecast_records = forecast_df.to_dict(
        orient="records"
    )

    avg_load = forecast_df[
        "Forecast_Wh"
    ].mean()

    for row in forecast_records:

        value = row["Forecast_Wh"]

        if value < avg_load * 0.9:

            row["zone"] = "Low"

        elif value > avg_load * 1.1:

            row["zone"] = "High"

        else:

            row["zone"] = "Medium"

    return forecast_df, forecast_records


def get_metrics():

    metrics = {}

    try:

        with open(
            "results/model_metrics.txt",
            "r"
        ) as f:

            for line in f:

                if ":" in line:

                    key, value = (
                        line.strip().split(":")
                    )

                    metrics[
                        key.lower()
                    ] = value.strip()

    except FileNotFoundError:

        metrics = {

            "mae": "0.0244",
            "rmse": "0.0544",
            "r2": "0.5905"

        }

    return metrics


def get_recommendations():

    try:

        with open(
            "results/recommendations.txt",
            "r"
        ) as f:

            return [
                line.strip()
                for line in f.readlines()
            ]

    except FileNotFoundError:

        return []


def get_peak_hours():

    try:

        with open(
            "results/peak_hours.txt",
            "r"
        ) as f:

            return [
                line.strip()
                for line in f.readlines()
            ]

    except FileNotFoundError:

        return []




@app.route("/")
def dashboard():

    forecast_df, forecast_records = (
        get_forecast_data()
    )

    times = forecast_df[
        "Time"
    ].tolist()

    values = forecast_df[
        "Forecast_Wh"
    ].tolist()

    recommendations = (
        get_recommendations()
    )

    peak_hours = (
        get_peak_hours()
    )

    return render_template(

        "index.html",

        recommendations=recommendations,

        peak_hours=peak_hours,

        times=times,

        values=values

    )



@app.route("/forecast")
def forecast():

    forecast_df, forecast_records = (
        get_forecast_data()
    )

    return render_template(

        "forecast.html",

        forecast=forecast_records

    )


@app.route("/analytics")
def analytics():

    metrics = get_metrics()

    return render_template(

        "analytics.html",

        metrics=metrics

    )



@app.route("/experiments")
def experiments():

    experiments = [

        [
            "Baseline",
            24,
            0.0240,
            0.0551,
            0.5805
        ],

        [
            "Reduced Features",
            24,
            0.0315,
            0.0572,
            0.5460
        ],

        [
            "Seq48",
            48,
            0.0334,
            0.0573,
            0.5450
        ],

        [
            "Seq12 (Best)",
            12,
            0.0244,
            0.0544,
            0.5905
        ]

    ]

    return render_template(

        "experiments.html",

        experiments=experiments

    )



@app.route("/about")
def about():

    return render_template(
        "about.html"
    )



if __name__ == "__main__":

    app.run(
        debug=True
    )