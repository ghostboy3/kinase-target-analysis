import streamlit as st
import plotly.express as px
import pandas as pd

def show_merge_tab():
    st.set_page_config(page_title="DataFrame Merger", layout="wide")

    st.title("Merge Two DataFrames")

    # Upload CSV files
    st.header("Upload csv, tsv, or xlsx dataframes")
    file1 = st.file_uploader("Upload First File", type=["csv", "tsv", "xlsx"])
    file2 = st.file_uploader("Upload Second File", type=["csv", "tsv", "xlsx"])

    if file1 and file2:
        if file1.name.endswith(".csv"):
            df1 = pd.read_csv(file1)
        elif file1.name.endswith(".tsv"):
            df1 = pd.read_csv(file1, "\t")
        else:
            df1 = pd.read_excel(file1)
        
        if file2.name.endswith(".csv"):
            df2 = pd.read_csv(file2)
        elif file2.name.endswith(".tsv"):
            df2 = pd.read_csv(file2, "\t")
        else:
            df2 = pd.read_excel(file2)
            st.subheader("First DataFrame")
        st.dataframe(df1)

        st.subheader("Second DataFrame")
        st.dataframe(df2)

        st.markdown("---")
        st.subheader("Merge Configuration")

        # Merge Keys
        merge_col1 = st.selectbox("Select merge column from First DataFrame", df1.columns)
        merge_col2 = st.selectbox("Select merge column from Second DataFrame", df2.columns)
        how = st.selectbox("Select merge method", ["inner", "outer", "left", "right"])
        st.markdown('<a href="https://www.w3schools.com/sql/sql_join.asp" target="_blank">Learn more about merge methods</a>', unsafe_allow_html=True)

        # Column selections
        st.markdown("Columns to Include in Merged DataFrame")
        col3, col4 = st.columns(2)
        with col3:
            cols1 = st.multiselect("Columns from First DataFrame", options=df1.columns.tolist(), default=list(df1.columns))
        with col4:
            cols2 = st.multiselect("Columns from Second DataFrame", options=df2.columns.tolist(), default=list(df2.columns))

        if st.button("Merge DataFrames"):
            try:
                # Filter selected columns before merge (must keep the merge keys)
                df1_filtered = df1[cols1] if merge_col1 in cols1 else df1[[merge_col1] + [c for c in cols1 if c != merge_col1]]
                df2_filtered = df2[cols2] if merge_col2 in cols2 else df2[[merge_col2] + [c for c in cols2 if c != merge_col2]]

                merged_df = pd.merge(df1_filtered, df2_filtered, left_on=merge_col1, right_on=merge_col2, how=how)
                st.success("Merge successful!")

                st.subheader("Merged DataFrame")
                st.dataframe(merged_df)

                csv = merged_df.to_csv(index=False).encode("utf-8")
                st.download_button("Download Merged CSV", data=csv, file_name="merged.csv", mime="text/csv")

            except Exception as e:
                st.error(f"Merge failed: {e}")
    else:
        st.info("Upload files to get started.")
