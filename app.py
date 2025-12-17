import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import detrend, savgol_filter, find_peaks

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Student Academic Performance Analysis",
    layout="wide"
)

st.title("📊 Student Academic Performance Analysis (SciPy + Time Series)")

# ------------------ File Upload ------------------
uploaded_file = st.file_uploader(
    "📂 Upload Excel File (Academic Year vs Marks)",
    type=["xlsx"]
)

# ------------------ Main Logic ------------------
if uploaded_file is not None:

    # Load Excel
    df = pd.read_excel(uploaded_file)

    # Show raw data
    st.subheader("📋 Raw Dataset")
    st.dataframe(df.head())

    # ------------------ Data Preprocessing ------------------
    df['Academic_Year'] = df['Academic_Year'].str.slice(0, 4).astype(int)
    df['Academic_Year'] = pd.to_datetime(df['Academic_Year'], format='%Y')
    df.set_index('Academic_Year', inplace=True)

    df['Marks'] = pd.to_numeric(df['Marks'])

    # ------------------ SciPy Processing ------------------
    marks_data = df['Marks'].values

    # Detrending
    df['Detrended_Marks'] = detrend(marks_data)

    # Safe window length for Savitzky–Golay
    window_length = min(21, len(df))
    if window_length % 2 == 0:
        window_length -= 1

    df['Smoothed_Marks'] = savgol_filter(
        df['Marks'], window_length=window_length, polyorder=3
    )

    # Year-wise change
    df['Marks_Change'] = df['Smoothed_Marks'].diff()

    # Peak detection
    peaks, _ = find_peaks(
        df['Smoothed_Marks'],
        height=df['Smoothed_Marks'].mean()
    )

    df['Peaks'] = False
    df.loc[df.index[peaks], 'Peaks'] = True

    # ------------------ Student Selection ------------------
    st.sidebar.header("🎓 Student Filter")

    student_id = st.sidebar.selectbox(
        "Select Student ID",
        df['Student_ID'].unique()
    )

    student_df = df[df['Student_ID'] == student_id]
    student_name = student_df['Student_Name'].iloc[0]

    st.sidebar.success(f"Student Name: {student_name}")

    st.subheader("📊 Processed Student Data")
    st.dataframe(student_df)

    # ------------------ Plot 1: Marks Trend ------------------
    st.subheader("📈 Marks Trend")
