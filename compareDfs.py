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

        # Show column selection options (only use common columns)
        common_columns = set(dataframes[0].columns)
        for df in dataframes[1:]:
            common_columns.intersection_update(set(df.columns))
        
        if not common_columns:
            st.error("No common columns across all CSV files.")
        else:
            selected_column = st.selectbox("Select column to graph", sorted(common_columns))

            remove_nan = st.checkbox("Remove NaN or empty values", value=True)

            # Prepare data for graphs
            processed_dfs = []
            for df in dataframes:
                column_data = df[selected_column].dropna() if remove_nan else df[selected_column]
                value_counts = column_data.value_counts().sort_index()
                processed_dfs.append(value_counts)

            ## --- Clustered Bar Graph ---
            fig_clustered = go.Figure()
            all_categories = sorted(set().union(*[df.index for df in processed_dfs]))

            for idx, counts in enumerate(processed_dfs):
                y_values = [counts.get(cat, 0) for cat in all_categories]
                fig_clustered.add_trace(go.Bar(
                    x=all_categories,
                    y=y_values,
                    name=names[idx]
                ))

            fig_clustered.update_layout(
                title="Clustered Bar Graph (CSV Comparison)",
                barmode='group',
                xaxis_title=selected_column,
                yaxis_title='Count'
            )
            st.plotly_chart(fig_clustered, use_container_width=True)

            ## --- Combined Bar Graph ---
            combined_counts = sum(processed_dfs)
            combined_counts = combined_counts[combined_counts > 0] if remove_nan else combined_counts

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

    else:
        st.info("Please upload at least one CSV file.")
