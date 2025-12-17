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
st.write("Analyze student marks using **trend removal, smoothing, peaks, and year-wise change**.")

# ------------------ File Upload ------------------
uploaded_file = st.file_uploader(
    "📂 Upload Excel File (Academic Year vs Marks)",
    type=["xlsx"]
)

if uploaded_file is not None:
    # Load data
    df = pd.read_excel(uploaded_file)

    st.subheader("📋 Raw Dataset")
    st.dataframe(df.head())

    # ------------------ Data Preprocessing ------------------
    df['Academic_Year'] = df['Academic_Year'].str.slice(0, 4).astype(int)
    df['Academic_Year'] = pd.to_datetime(df['Academic_Year'], format='%Y')
    df.set_index('Academic_Year', inplace=True)

    df['Marks'] = pd.to_numeric(df['Marks'])

    # SciPy Processing
    marks_data = df['Marks'].values
    df['Detrended_Marks'] = detrend(marks_data)

    window_length = min(21, len(df) if len(df) % 2 != 0 else len(df) - 1)
    df['Smoothed_Marks'] = savgol_filter(df['Marks'], window_length, polyorder=3)

    df['Marks_Change'] = df['Smoothed_Marks'].diff()

    # Find Peaks
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
    st.sidebar.success(f"Student: **{student_name}**")

    st.subheader("📊 Processed Student Data")
    st.dataframe(student_df)

    # ------------------ Plot 1: Marks Trend ------------------
    st.subheader("📈 Marks Trend Analysis")

    fig1 = plt.figure(figsize=(12, 6))
    plt.plot(student_df.index, student_df['Marks'], label='Original Marks')
    plt.plot(student_df.index, student_df['Smoothed_Marks'], label='Smoothed Marks')
    plt.plot(
        student_df.index[student_df['Peaks']],
        student_df['Smoothed_Marks'][student_df['Peaks']],
        "o",
        label="Peaks"
    )

    plt.xlabel("Academic Year")
    plt.ylabel("Marks")
    plt.title("Original vs Smoothed Marks")
    plt.legend()
    plt.grid(True)

    st.pyplot(fig1)

    # ------------------ Plot 2: Detrended Data ------------------
    st.subheader("📉 Detrended Marks")

    fig2 = plt.figure(figsize=(12, 5))
    plt.plot(student_df.index, student_df['Detrended_Marks'])
    plt.axhline(0, linestyle="--")
    plt.xlabel("Academic Year")
    plt.ylabel("Detrended Marks")
    plt.title("Marks After Removing Trend")
    plt.grid(True)

    st.pyplot(fig2)

    # ------------------ Plot 3: Year-wise Change ------------------
    st.subheader("📊 Year-over-Year Marks Change")

    fig3 = plt.figure(figsize=(12, 5))
    plt.plot(student_df.index, student_df['Marks_Change'])
    plt.axhline(0, linestyle="--")
    plt.xlabel("Academic Year")
    plt.ylabel("Change in Marks")
    plt.title("Change in Smoothed Marks")
    plt.grid(True)

    st.pyplot(fig3)

    # ------------------ Download ------------------
    st.subheader("⬇️ Download Processed Data")
    st.download_button(
        label="Download as CSV",
        data=student_df.to_csv().encode("utf-8"),
        file_name="processed_student_marks.csv",
        mime="text/csv"
    )

else:
    st.info("👆 Please upload an Excel file to begin analysis.")

