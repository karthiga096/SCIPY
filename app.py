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

# ------------------ File Upload (HIDDEN LABEL) ------------------
uploaded_file = st.file_uploader(
    "",
    type=["xlsx"],
    label_visibility="collapsed"
)

# ------------------ Main Logic ------------------
if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    # Preprocess
    df['Academic_Year'] = df['Academic_Year'].str.slice(0, 4).astype(int)
    df['Academic_Year'] = pd.to_datetime(df['Academic_Year'], format='%Y')
    df.set_index('Academic_Year', inplace=True)

    df['Marks'] = pd.to_numeric(df['Marks'])

    # SciPy processing
    marks = df['Marks'].values
    df['Detrended_Marks'] = detrend(marks)

    window = min(21, len(df))
    if window % 2 == 0:
        window -= 1

    df['Smoothed_Marks'] = savgol_filter(df['Marks'], window, 3)
    df['Marks_Change'] = df['Smoothed_Marks'].diff()

    peaks, _ = find_peaks(df['Smoothed_Marks'], height=df['Smoothed_Marks'].mean())
    df['Peaks'] = False
    df.loc[df.index[peaks], 'Peaks'] = True

    # Sidebar
    st.sidebar.header("🎓 Student Filter")
    student_id = st.sidebar.selectbox("Student ID", df['Student_ID'].unique())

    student_df = df[df['Student_ID'] == student_id]
    student_name = student_df['Student_Name'].iloc[0]
    st.sidebar.success(f"Student: {student_name}")

    # Display data
    st.subheader("📋 Student Data")
    st.dataframe(student_df)

    # Plot 1
    st.subheader("📈 Marks Trend")
    fig1 = plt.figure(figsize=(12, 5))
    plt.plot(student_df.index, student_df['Marks'], label="Original")
    plt.plot(student_df.index, student_df['Smoothed_Marks'], label="Smoothed")
    plt.scatter(
        student_df.index[student_df['Peaks']],
        student_df['Smoothed_Marks'][student_df['Peaks']],
        label="Peaks"
    )
    plt.legend()
    plt.grid()
    st.pyplot(fig1)

    # Plot 2
    st.subheader("📉 Detrended Marks")
    fig2 = plt.figure(figsize=(12, 4))
    plt.plot(student_df.index, student_df['Detrended_Marks'])
    plt.axhline(0, linestyle="--")
    plt.grid()
    st.pyplot(fig2)

    # Plot 3
    st.subheader("📊 Year-wise Change")
    fig3 = plt.figure(figsize=(12, 4))
    plt.plot(student_df.index, student_df['Marks_Change'])
    plt.axhline(0, linestyle="--")
    plt.grid()
    st.pyplot(fig3)

    # Download
    st.download_button(
        "⬇️ Download CSV",
        student_df.to_csv().encode("utf-8"),
        "processed_student_marks.csv",
        "text/csv"
    )
