from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def dashboard():

    # Forecast Data
    forecast_df = pd.read_csv(
        "results/forecast_results.csv"
    )

    forecast_records = forecast_df.to_dict(
        orient="records"
    )

    # Recommendations
    with open(
        "results/recommendations.txt",
        "r"
    ) as f:

        recommendations = [
            line.strip()
            for line in f.readlines()
        ]

    # Peak Hours
    with open(
        "results/peak_hours.txt",
        "r"
    ) as f:

        peak_hours = [
            line.strip()
            for line in f.readlines()
        ]

    metrics = {
        "mae": "0.0244",
        "rmse": "0.0544",
        "r2": "0.5905"
    }

    return render_template(
        "index.html",
        metrics=metrics,
        forecast=forecast_records,
        recommendations=recommendations,
        peak_hours=peak_hours
    )

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)