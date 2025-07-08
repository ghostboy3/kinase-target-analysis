# TODO: Blank: Associated proteins, non protein kinases, and isoforms

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np


st.title("Upload and View DataFrame")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Determine file type and read accordingly
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully!")

        # Display the dataframe
        st.subheader("Preview of Data")
        st.dataframe(df)

        # Optional: Show basic info
        st.subheader("Basic Info")
        st.write("Shape:", df.shape)
        st.write("Columns:", list(df.columns))

        column = st.selectbox("Select a column to visualize", df.columns)
        df[column] = df[column].astype(str).str.strip()

        # Choose chart type
        chart_type = st.radio("Chart type", ["Bar Chart", "Pie Chart"])

        value_counts = df[column].value_counts().reset_index()
        value_counts.columns = [column, "Count"]

        # Plot
        if chart_type == "Bar Chart":
            fig = px.bar(value_counts, x=column, y="Count",
                        title=f"Bar Chart of {column}", text_auto=True)
        else:
            fig = px.pie(value_counts, names=column, values="Count",
                        title=f"Pie Chart of {column}")

        fig.update_layout(autosize=True, dragmode="zoom")
        st.plotly_chart(fig, use_container_width=True)


        # fig.update_layout(autosize=True, dragmode="zoom")
        # st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a file to begin.")
