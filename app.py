import streamlit as st

# Page config
st.set_page_config(page_title="Marks Difference Calculator", layout="centered")
st.title("📊 Marks Increase / Decrease Calculator")

st.write("Enter 2 academic years and their marks to see the change.")

# User input columns
col1, col2 = st.columns(2)

with col1:
    year1 = st.number_input("First Academic Year:", min_value=1800, max_value=3000, value=2023)
    mark1 = st.number_input("Marks for First Year:", min_value=0, max_value=100, value=50)

with col2:
    year2 = st.number_input("Second Academic Year:", min_value=1800, max_value=3000, value=2024)
    mark2 = st.number_input("Marks for Second Year:", min_value=0, max_value=100, value=55)

# Calculation
if st.button("Calculate Change"):
    difference = mark2 - mark1

    if difference > 0:
        status = "📈 Increased"
    elif difference < 0:
        status = "📉 Decreased"
    else:
        status = "⚖ No Change"

    # Display result
    st.subheader("Result")
    st.write(f"Marks from **{year1} → {year2}**: {mark1} → {mark2}")
    st.write(f"Difference: **{difference}**")
    st.write(f"Status: **{status}**")
