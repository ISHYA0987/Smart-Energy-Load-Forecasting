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

def generate_ai_insights(forecast_df):

    values = forecast_df["Forecast_Wh"].tolist()
    times = forecast_df["Time"].tolist()

    highest = max(values)
    lowest = min(values)

    highest_time = times[values.index(highest)]
    lowest_time = times[values.index(lowest)]

    average = sum(values) / len(values)

    insights = []

    # Peak Load
    insights.append({
        "icon": "bi-lightning-charge-fill",
        "color": "warning",
        "title": "Peak Load Expected",
        "message": f"Highest demand is expected around {highest_time} ({highest:.1f} Wh)."
    })

    # Best Appliance Time
    insights.append({
        "icon": "bi-clock-history",
        "color": "primary",
        "title": "Best Time for Heavy Appliances",
        "message": f"Use washing machines, heaters, or dishwashers near {lowest_time} when demand is lowest."
    })

    # Load Balance
    high_hours = len([v for v in values if v > average * 1.10])

    if high_hours >= 5:

        status = "High"

        msg = "Several high-load periods are predicted today. Consider shifting heavy appliance usage."

    elif high_hours >= 3:

        status = "Moderate"

        msg = "Energy demand is balanced with a few peak periods."

    else:

        status = "Low"

        msg = "Energy demand remains stable throughout the day."

    insights.append({
        "icon": "bi-bar-chart-line-fill",
        "color": "success",
        "title": "Load Analysis",
        "message": msg
    })

    # Savings Estimate
    saving = round((highest-average)/highest*100,1)

    insights.append({
        "icon":"bi-stars",
        "color":"success",
        "title":"Estimated Saving",
        "message":f"Scheduling heavy appliances during low-load periods may reduce consumption by approximately {saving}%."
    })

    return insights

def get_peak_hour_details(forecast_df):

    top = forecast_df.nlargest(5, "Forecast_Wh")

    peak_hours = []

    for _, row in top.iterrows():

        peak_hours.append({

            "time": row["Time"],

            "load": round(row["Forecast_Wh"], 2),

            "status": "High"

        })

    return peak_hours


def get_appliance_schedule(forecast_df):

    low = forecast_df.nsmallest(4, "Forecast_Wh")

    appliances = [

        "Washing Machine",

        "Dishwasher",

        "Water Heater",

        "EV Charging"

    ]

    schedule = []

    for appliance, (_, row) in zip(appliances, low.iterrows()):

        schedule.append({

            "appliance": appliance,

            "time": row["Time"],

            "load": round(row["Forecast_Wh"],2)

        })

    return schedule


@app.route("/")
def dashboard():

    forecast_df, forecast_records = get_forecast_data()

    times = forecast_df["Time"].tolist()
    values = forecast_df["Forecast_Wh"].tolist()

    recommendations = get_recommendations()
    ai_insights = generate_ai_insights(forecast_df)
    peak_hours = get_peak_hour_details(forecast_df)

    appliance_schedule = get_appliance_schedule(forecast_df)

    metrics = get_metrics()

   

    next_prediction = round(values[0], 2)
    next_time = times[0]

    highest = max(values)
    highest_time = times[values.index(highest)]

    lowest = min(values)
    lowest_time = times[values.index(lowest)]

    average = round(sum(values) / len(values), 2)

    total_energy = round(sum(values) / 1000, 2)     # kWh

    high_count = len(
        [v for v in values if v > average * 1.10]
    )

    medium_count = len(
        [v for v in values
         if average * 0.90 <= v <= average * 1.10]
    )

    low_count = len(
        [v for v in values if v < average * 0.90]
    )

    return render_template(

        "index.html",

        
        times=times,
        values=values,
        peak_hours=peak_hours,
        appliance_schedule=appliance_schedule,
        recommendations=recommendations,
        ai_insights=ai_insights,

        
        next_prediction=next_prediction,
        next_time=next_time,
        total_energy=total_energy,
        high_count=high_count,

        
        highest=round(highest,2),
        highest_time=highest_time,

        lowest=round(lowest,2),
        lowest_time=lowest_time,

        average=average,

        
        high_load=high_count,
        medium_load=medium_count,
        low_load=low_count,

        
        model_name="LSTM",
        sequence_length=12,

        
        metrics=metrics

    )

@app.route("/forecast")
def forecast():

    forecast_df, forecast_records = get_forecast_data()

    highest = round(forecast_df["Forecast_Wh"].max(), 2)
    lowest = round(forecast_df["Forecast_Wh"].min(), 2)
    average = round(forecast_df["Forecast_Wh"].mean(), 2)
    total = len(forecast_df)
    peak_row = forecast_df.loc[forecast_df["Forecast_Wh"].idxmax()]

    low_row = forecast_df.loc[forecast_df["Forecast_Wh"].idxmin()]

    return render_template(

        "forecast.html",

        forecast=forecast_records,

        highest=highest,
        lowest=lowest,
        average=average,
        total=total,
        peak_hour = peak_row["Time"],
        peak_value = round(peak_row["Forecast_Wh"], 2),

        low_hour = low_row["Time"],
        low_value = round(low_row["Forecast_Wh"], 2)

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

@app.route("/model")
def model():

    metrics = get_metrics()

    model_info = {

        "name": "LSTM",

        "sequence": 12,

        "forecast": "24 Hours",

        "dataset": "Smart Meter",

        "optimizer": "Adam",

        "epochs": 100,

        "batch_size": 32,

        "learning_rate": 0.001

    }

    return render_template(

        "model.html",

        metrics=metrics,

        model=model_info

    )


if __name__ == "__main__":

    app.run(
        debug=True
    )