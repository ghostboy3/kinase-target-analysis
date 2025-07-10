import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def show_analyze_tab():

    st.title("Analyze DataFrame")

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

            st.subheader("Basic Info")
            st.write("Shape:", df.shape)
            # st.write("Columns:", list(df.columns))
            st.write("Columnsy")
            st.dataframe(df.dtypes.reset_index().rename(columns={0: 'Type', 'index': 'Column'}))

            st.subheader("Visulize Data")
            column = st.selectbox("Select a column to visualize", df.columns)
            df[column] = df[column].astype(str).str.strip()

            value_counts = df[column].value_counts().reset_index()
            value_counts.columns = [column, "Count"]
            st.dataframe(value_counts)
            # Choose chart type
            chart_type = st.radio("Chart type", ["Bar Chart", "Pie Chart"])


            # Plot
            if chart_type == "Bar Chart":
                fig = px.bar(value_counts, x=column, y="Count",
                            title=f"Bar Chart of {column}", text_auto=True)
            else:
                fig = px.pie(value_counts, names=column, values="Count",
                            title=f"Pie Chart of {column}")
                # fig.update_traces(textinfo='label+percent+value')
                # Expand margins and enable zooming
                # fig.update_layout(
                # margin=dict(t=60, b=120, l=60, r=60),  # prevent clipping
                # height=700,  # increase height to fit long labels
                # )

                # Enable zoom and pan
                # fig.update_layout(
                # dragmode='pan',
                # )



            fig.update_layout(autosize=True, dragmode="zoom")
            st.plotly_chart(fig, use_container_width=True)


            st.subheader("Graph Data")

            numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

            if len(numeric_cols) < 2:
                st.warning("Need at least two numeric columns for plotting.")
            else:
                # Select chart type
                chart_type = st.radio("Select chart type", ["Line Plot", "Scatter Plot"])

                # Axis selectors
                x_axis = st.selectbox("X-axis", options=numeric_cols)
                y_axis = st.selectbox("Y-axis", options=[col for col in numeric_cols if col != x_axis])

                # Plot
                if chart_type == "Line Plot":
                    fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
                else:
                    fig = px.scatter(df, x=x_axis, y=y_axis,  title=f"{y_axis} vs {x_axis}")

                fig.update_layout(autosize=True, dragmode="zoom")
                st.plotly_chart(fig, use_container_width=True)


            # fig.update_layout(autosize=True, dragmode="zoom")
            # st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.info("Please upload a file to begin.")