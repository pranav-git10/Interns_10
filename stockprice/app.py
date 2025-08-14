import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from keras.models import load_model
from copy import deepcopy


st.header('Stock Price Prediction Model')
# Custom CSS for the entire webpage
custom_css = """
    <style>
        body {
            background-color: #001f3f; /* Dark Blue */
            color: white;
        }
        .css-18e3th9 {
            padding-top: 60px; /* Adjust main content padding */
        }
        .css-1d391kg {
            display: none; /* Hide default sidebar */
        }
        .navbar {
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 1;
            background-color: #0074D9; /* Light Blue */

        }
        .navbar input[type="file"] {
            display: none;
        }
        .navbar label {
            cursor: pointer;
            padding: 5px 10px;
            border-radius: 5px;
        }
    </style>
"""

# Apply custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Navbar layout
st.markdown("""
    <div class="navbar">
        <label for="file-upload">Upload CSV</label>
        <input type="file" id="file-upload" name="file-upload" accept=".csv" onchange="window.dispatchEvent(new Event('file-uploaded'));">
        <span id="date-inputs"></span>
    </div>
""", unsafe_allow_html=True)

# JavaScript to handle file upload and date inputs
st.markdown("""
    <script>
        const fileInput = document.getElementById('file-upload');
        fileInput.addEventListener('change', (event) => {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = (e) => {
                const text = e.target.result;
                window.dispatchEvent(new CustomEvent('file-content', { detail: text }));
            };
            reader.readAsText(file);
        });

        window.addEventListener('file-uploaded', () => {
            const dateInputsContainer = document.getElementById('date-inputs');
            dateInputsContainer.innerHTML = `
                <input type="date" id="start-date" name="start-date">
                <input type="date" id="end-date" name="end-date">
            `;
        });

        window.addEventListener('file-content', (e) => {
            const fileContent = e.detail;
            const data = new Blob([fileContent], { type: 'text/csv' });
            const file = new File([data], 'uploaded.csv');
            const event = new Event('change');
            document.getElementById('file-upload').files = new FileList(file);
            document.getElementById('file-upload').dispatchEvent(event);
        });
    </script>
""", unsafe_allow_html=True)

# Placeholder for Streamlit file uploader (to be hidden)
uploaded_file = st.file_uploader("", type=['csv'])

# Function to convert string to datetime
def str_to_datetime(s):
    split = s.split('-')
    year, month, day = int(split[0]), int(split[1]), int(split[2])
    return datetime.datetime(year=year, month=month, day=day)

# Function to create windowed dataframe
def df_to_windowed_df(dataframe, first_date_str, last_date_str, n=3):
    first_date = str_to_datetime(first_date_str)
    last_date = str_to_datetime(last_date_str)

    target_date = first_date

    dates = []
    X, Y = [], []

    last_time = False
    while True:
        df_subset = dataframe.loc[:target_date].tail(n + 1)

        if len(df_subset) != n + 1:
            target_date += datetime.timedelta(days=1)
            if target_date > last_date:
                break
            continue

        values = df_subset['Close'].to_numpy()
        x, y = values[:-1], values[-1]

        dates.append(target_date)
        X.append(x)
        Y.append(y)

        next_week = dataframe.loc[target_date:target_date + datetime.timedelta(days=7)]
        next_datetime_str = str(next_week.head(2).tail(1).index.values[0])
        next_date_str = next_datetime_str.split('T')[0]
        year, month, day = next_date_str.split('-')
        next_date = datetime.datetime(day=int(day), month=int(month), year=int(year))

        if last_time:
            break

        target_date = next_date

        if target_date == last_date:
            last_time = True

    ret_df = pd.DataFrame({})
    ret_df['Target Date'] = dates

    X = np.array(X)
    for i in range(0, n):
        X[:, i]
        ret_df[f'Target-{n - i}'] = X[:, i]

    ret_df['Target'] = Y

    return ret_df

# Function to convert windowed dataframe to date, X, and y
def windowed_df_to_date_X_y(windowed_dataframe):
    df_as_np = windowed_dataframe.to_numpy()

    dates = df_as_np[:, 0]

    middle_matrix = df_as_np[:, 1:-1]
    X = middle_matrix.reshape((len(dates), middle_matrix.shape[1], 1))

    Y = df_as_np[:, -1]

    return dates, X.astype(np.float32), Y.astype(np.float32)

# Sidebar (now converted to a top navbar)
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df = df[['Date', 'Close']]
    df['Date'] = df['Date'].apply(str_to_datetime)
    df.index = df.pop('Date')

    # Dynamic date inputs
    min_date = df.index.min().date()
    max_date = df.index.max().date()

    start_date = st.sidebar.date_input('Start date', min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.sidebar.date_input('End date', min_value=min_date, max_value=max_date, value=max_date)

    if start_date >= end_date:
        st.error('Error: End date must be after start date.')
    else:
        # Convert date inputs to strings
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        # Generate windowed dataframe
        windowed_df = df_to_windowed_df(df, start_date_str, end_date_str, n=3)
        if windowed_df is not None and not windowed_df.empty:
            dates, X, y = windowed_df_to_date_X_y(windowed_df)

            # Split data into train, validation, and test sets
            q_80 = int(len(dates) * .8)
            q_90 = int(len(dates) * .9)

            dates_train, X_train, y_train = dates[:q_80], X[:q_80], y[:q_80]
            dates_val, X_val, y_val = dates[q_80:q_90], X[q_80:q_90], y[q_80:q_90]
            dates_test, X_test, y_test = dates[q_90:], X[q_90:], y[q_90:]

            # Load the trained model
            model = load_model('Stock_Predictions_Model.keras')

            # Predictions
            train_predictions = model.predict(X_train).flatten()
            val_predictions = model.predict(X_val).flatten()
            test_predictions = model.predict(X_test).flatten()

            # Plot predictions for train, validation, and test sets
            st.subheader('Training Predictions')
            plt.figure(figsize=(14, 7))
            plt.plot(dates_train, train_predictions, label='Training Predictions')
            plt.plot(dates_train, y_train, label='Training Observations')
            plt.legend()
            st.pyplot(plt)

            st.subheader('Validation Predictions')
            plt.figure(figsize=(14, 7))
            plt.plot(dates_val, val_predictions, label='Validation Predictions')
            plt.plot(dates_val, y_val, label='Validation Observations')
            plt.legend()
            st.pyplot(plt)

            st.subheader('Testing Predictions')
            plt.figure(figsize=(14, 7))
            plt.plot(dates_test, test_predictions, label='Testing Predictions')
            plt.plot(dates_test, y_test, label='Testing Observations')
            plt.legend()
            st.pyplot(plt)

            # Combined plot
            st.subheader('Combined Plot')
            plt.figure(figsize=(14, 7))
            plt.plot(dates_train, train_predictions, label='Training Predictions')
            plt.plot(dates_train, y_train, label='Training Observations')
            plt.plot(dates_val, val_predictions, label='Validation Predictions')
            plt.plot(dates_val, y_val, label='Validation Observations')
            plt.plot(dates_test, test_predictions, label='Testing Predictions')
            plt.plot(dates_test, y_test, label='Testing Observations')
            plt.legend()
            st.pyplot(plt)

            # Recursive Predictions
            recursive_predictions = []
            recursive_dates = np.concatenate([dates_val, dates_test])

            last_window = deepcopy(X_train[-1])
            for _ in recursive_dates:
                next_prediction = model.predict(np.array([last_window])).flatten()
                recursive_predictions.append(next_prediction)
                last_window = np.roll(last_window, -1)
                last_window[-1] = next_prediction

            st.subheader('Recursive Predictions')
            plt.figure(figsize=(14, 7))
            plt.plot(dates_train, train_predictions, label='Training Predictions')
            plt.plot(dates_train, y_train, label='Training Observations')
            plt.plot(dates_val, val_predictions, label='Validation Predictions')
            plt.plot(dates_val, y_val, label='Validation Observations')
            plt.plot(dates_test, test_predictions, label='Testing Predictions')
            plt.plot(dates_test, y_test, label='Testing Observations')
            plt.plot(recursive_dates, recursive_predictions, label='Recursive Predictions')
            plt.legend()
            st.pyplot(plt)
