# Smart Energy Load Forecasting

## Overview

Smart Energy Load Forecasting is a machine learning-based web application that predicts future household energy consumption and provides intelligent recommendations for efficient energy usage.

The system uses a Long Short-Term Memory (LSTM) neural network to analyze historical appliance energy consumption data and forecast future electricity demand. Based on predicted load patterns, the application identifies peak consumption periods and suggests optimal times for operating household appliances.

---

## Features

### Energy Consumption Forecasting

* Predicts future household energy usage using an LSTM model.
* Generates a 24-hour energy consumption forecast.

### Peak Load Detection

* Detects high-load periods from forecasted values.
* Highlights peak hours to help users avoid excessive energy usage.

### Smart Recommendations

* Suggests optimal times for:

  * Washing machines
  * Water heaters
  * Device charging
* Helps distribute appliance usage to reduce peak demand.

### Load Zone Classification

* Classifies forecasted consumption into:

  * Low Load
  * Medium Load
  * High Load
* Provides a visual understanding of future energy demand.

### Interactive Dashboard

* Built using Flask.
* Displays:

  * Forecast charts
  * Peak hours
  * Recommendations
  * Forecast details
  * Model analytics

### Model Analytics

* Displays:

  * MAE
  * RMSE
  * R² Score
* Includes feature importance analysis and training history.

---

## Dataset

### Dataset Used

**Appliances Energy Prediction Dataset**

Source:
https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction

### Dataset Information

The dataset contains:

* Appliance energy consumption
* Indoor temperatures
* Indoor humidity
* Outdoor weather conditions
* Timestamp information

Total Records:

* 19,735 samples

Sampling Frequency:

* Every 10 minutes

---

## Project Workflow

### 1. Data Cleaning

* Removed unnecessary columns
* Converted timestamps
* Handled missing values
* Generated time-based features

### 2. Exploratory Data Analysis (EDA)

* Correlation analysis
* Feature importance analysis
* Consumption pattern analysis

### 3. Feature Engineering

Features used:

* Appliances
* T_out
* RH_out
* Windspeed
* T1
* RH_1
* T2
* RH_2
* hour
* day_of_week
* month
* is_weekend

### 4. Data Preprocessing

* MinMax Scaling
* Sequence generation for LSTM

### 5. Model Training

* LSTM Neural Network
* Sequence Length = 12
* Hidden Size = 64
* Number of Layers = 2
* Dropout = 0.2

### 6. Forecast Generation

* Recursive 24-hour forecasting
* Peak hour identification
* Recommendation generation

### 7. Dashboard Development

* Flask-based web interface
* Interactive visualization using Chart.js

---

## Model Architecture

LSTM Configuration:

* Input Features: 12
* Sequence Length: 12
* Hidden Size: 64
* Number of LSTM Layers: 2
* Dropout: 0.2
* Optimizer: Adam
* Loss Function: Mean Squared Error (MSE)

---

## Final Model Performance

| Metric   | Value  |
| -------- | ------ |
| MAE      | 0.0244 |
| RMSE     | 0.0544 |
| R² Score | 0.5905 |

---

## Experiments Performed

| Experiment         | MAE    | RMSE   | R²     |
| ------------------ | ------ | ------ | ------ |
| Baseline (Seq=24)  | 0.0240 | 0.0551 | 0.5805 |
| Reduced Features   | 0.0315 | 0.0572 | 0.5460 |
| Sequence Length 48 | 0.0334 | 0.0573 | 0.5450 |
| Sequence Length 12 | 0.0244 | 0.0544 | 0.5905 |

Best Model:

* Sequence Length = 12
* R² = 0.5905

---

## Project Structure

```text
Smart-Energy-Load-Forecasting/

│
├── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   ├── lstm_model.pth
│   └── scaler.pkl
│
├── notebooks/
│   ├── 01_data_cleaning.py
│   └── 02_eda.py
│
├── src/
│   ├── model.py
│   ├── preprocess.py
│   ├── create_sequences.py
│   ├── train.py
│   ├── predict.py
│   ├── forecast24.py
│   ├── feature_importance.py
│   └── generate_dashboard_data.py
│
├── static/
│
├── templates/
│
├── results/
│
├── requirements.txt
│
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Smart-Energy-Load-Forecasting
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the Project

Generate dashboard data:

```bash
python src/generate_dashboard_data.py
```

Start Flask server:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Technologies Used

* Python
* Flask
* PyTorch
* Pandas
* NumPy
* Scikit-Learn
* Matplotlib
* Chart.js
* HTML
* CSS
* Bootstrap

---

## Future Improvements

* Real-time smart meter integration
* Weather-aware forecasting
* Renewable energy optimization
* Mobile application support
* Advanced deep learning models
* Live energy monitoring dashboard

---

## Author

**Ishya Bommireddy**

Computer Science and Engineering Student

RGUKT Nuzvid

Summer Internship Project
