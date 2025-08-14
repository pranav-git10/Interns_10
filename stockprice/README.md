# Stock Price Prediction

Welcome to the Stock Price Prediction project! This repository contains tools and scripts to predict stock prices using historical data and machine learning techniques, specifically with a Long Short-Term Memory (LSTM) neural network. You can visualize the results interactively through a Streamlit application.

# Description
This project aims to provide an end-to-end solution for stock price prediction using deep learning. We leverage the power of LSTM networks, which are well-suited for time series forecasting tasks, to predict the closing prices of stocks based on historical data.

# How It Works
Data Loading: Load historical stock price data from a CSV file.
Data Transformation: Transform the data into a suitable format for time series forecasting, creating windowed data frames for model input.
Model Training: Train an LSTM model to predict future stock prices.
Prediction and Visualization: Use the trained model to make predictions and visualize the results using an interactive Streamlit application.

## Dataset

Your dataset should be a CSV file with the following columns:

- `Date`: The date of the stock price observation.
- `Close`: The closing price of the stock on that date.

A sample dataset (`MSFT-2.csv`) with historical stock prices for Microsoft (MSFT) is included.

## Model Training

The `model_training.py` script handles the training process:

1. **Load and preprocess the dataset:** Convert date strings to datetime objects and set the date as the index.
2. **Create windowed data:** Generate input-output pairs for the LSTM model.
3. **Train the model:** Train the LSTM model and save it for later use.

To train the model, run:
```sh
python model_training.py
```

## Streamlit Application

The Streamlit application (`app.py`) allows you to:

- Upload a stock price CSV file.
- Select date ranges.
- Visualize the model's predictions.


Thank you for checking out this project! If you have any questions or feedback, please reach out. Happy coding and predicting!
