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

        # column = st.selectbox("Select a column to visualize", df.columns)

        # # Chart type selector
        # chart_type = st.radio("Choose chart type", ["Bar Chart", "Pie Chart"])

        # # Calculate value counts
        # value_counts = df[column].value_counts()

        # # Plot
        # fig, ax = plt.subplots()
        # if chart_type == "Bar Chart":
        #     value_counts.plot(kind='bar', ax=ax)
        #     ax.set_ylabel("Count")
        #     ax.set_title(f"Bar Chart of {column}")
        # else:
        #     value_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90)
        #     ax.set_ylabel("")
        #     ax.set_title(f"Pie Chart of {column}")
        #     ax.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle

        # st.pyplot(fig)

        column = st.selectbox("Select a column to visualize", df.columns)
        df[column] = df[column].astype(str).str.strip()

        # Choose chart type
        chart_type = st.radio("Chart type", ["Bar Chart", "Pie Chart"])

        # Count value frequencies
        value_counts = df[column].value_counts().reset_index()
        # print(value_counts)
        value_counts.columns = ["Value", "Num"]  # keep it generic

        # print(value_counts.columns)
        # Plot
        if chart_type == "Bar Chart":
            fig = px.bar(
                value_counts,
                x=column,
                y="Count",
                title=f"Bar Chart of {column}",
                text_auto=True,
            )
        else:
            # random_x = [100, 2000, 550]
            # names = ['A', 'B', 'C']

            # fig = px.pie(values=random_x, names=names)

            # st.dataframe(value_counts)
            # # st.text(type(value_counts["Count"][0]))
            # fig = px.pie(
            #     value_counts,
            #     values="Num",
            #     names="Value",
            #     title=f"Pie Chart of {column}",
            # )

            # fig.update_layout(autosize=True, dragmode="zoom")
            # st.plotly_chart(fig, use_container_width=True)

            x1 = np.random.randn(200) - 2
            x2 = np.random.randn(200)
            x3 = np.random.randn(200) + 2

            # Group data together
            hist_data = [x1, x2, x3]

            group_labels = ['Group 1', 'Group 2', 'Group 3']

            # Create distplot with custom bin_size
            fig = ff.create_distplot(
                    hist_data, group_labels, bin_size=[.1, .25, .5])

    # Plot!
            st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a file to begin.")
