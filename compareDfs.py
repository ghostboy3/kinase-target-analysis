#TODO: bar chart comaring lengths of data

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def showCompareTab():
    st.title("Multi data Bar Graph Comparison Tool")

    # Upload multiple CSV files
    uploaded_files = st.file_uploader("Upload CSV, XLSX, or TSV files", type=["csv", "tsv", "xlsx"], accept_multiple_files=True)

    if uploaded_files:
        dataframes = []
        names = []

        # Read all CSVs
        for uploaded_file in uploaded_files:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".tsv"):
                df = pd.read_csv(uploaded_file, delimiter="\t")
            else:
                df = pd.read_excel(uploaded_file)
            dataframes.append(df)
            names.append(uploaded_file.name)
        drop_nans = st.checkbox("Remove NaN or empty values")
        if drop_nans:
            # df = df.dropna()
            dataframes = [df.dropna() for df in dataframes]




        # Show column selection options (only use common columns)
        common_columns = set(dataframes[0].columns)
        for df in dataframes[1:]:
            common_columns.intersection_update(set(df.columns))
        
        if not common_columns:
            st.error("No common columns across all CSV files.")
        else:
            selected_column = st.selectbox("Select column to graph", sorted(common_columns))

            # remove_nan = st.checkbox("Remove NaN or empty values", value=True)

            # Prepare data for graphs
            processed_dfs = []
            for df in dataframes:
                column_data = df[selected_column]
                value_counts = column_data.value_counts().sort_index()
                processed_dfs.append(value_counts)
            custom_labels = []
            st.subheader("Customize Bar Labels")
            for i, name in enumerate(names):
                label = st.text_input(f"Label for {name}", value=name)
                custom_labels.append(label)
            x_axis = st.text_input(f"X Axis label")
            y_axis = st.text_input(f"Y Axis label")

            ## --- Clustered Bar Graph ---
            fig_clustered = go.Figure()
            all_categories = sorted(set().union(*[df.index for df in processed_dfs]))

            for idx, counts in enumerate(processed_dfs):
                y_values = [counts.get(cat, 0) for cat in all_categories]
                fig_clustered.add_trace(go.Bar(
                    x=all_categories,
                    y=y_values,
                    name=custom_labels[idx]
                ))

            fig_clustered.update_layout(
                title="Clustered Bar Graph",
                barmode='group',
                xaxis_title=x_axis,
                yaxis_title=y_axis
            )
            st.plotly_chart(fig_clustered, use_container_width=True)


            ## --- Combined Bar Graph ---
            combined_counts = sum(processed_dfs)
            combined_counts =  combined_counts

            fig_combined = go.Figure(go.Bar(
                x=combined_counts.index,
                y=combined_counts.values,
                name='Combined'
            ))
            fig_combined.update_layout(
                title="Combined Bar Graph",
                xaxis_title=selected_column,
                yaxis_title='Total Count'
            )
            st.plotly_chart(fig_combined, use_container_width=True)
            

            # Lenght bar graph
            st.subheader("Length of Databases")
            # df = df.dropna()

            row_counts = [len(df.dropna())  for df in dataframes]
            
            fig_rows = go.Figure(go.Bar(
                x=custom_labels,
                y=row_counts,
                marker_color='orange',
                name='Row Count',
                text=row_counts,
                textposition='auto'
            ))


            fig_rows.update_layout(
                xaxis_title=x_axis,
                yaxis_title=y_axis,
                title="Comparison of Dataset Sizes"
            )

            st.plotly_chart(fig_rows, use_container_width=True)


    else:
        st.info("Please upload at least one CSV file.")
