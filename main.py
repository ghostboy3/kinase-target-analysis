import pandas as pd

# Load the Excel sheets
kinase_df = pd.read_excel("Kinase_list.xlsx")
abpp_df = pd.read_excel("ABPP_hek293_candidates_filtered_tyrosine_kinases_kc.xlsx")

# # Clean up: get only the first part of the Kinbase classification
kinase_df["Kinase Classification"] = kinase_df["Kinbase classification"].str.split(":").str[0].str.strip()
print(kinase_df.columns)

merged_df = abpp_df.merge(
    kinase_df[["HGNC ", "Kinase Classification"]],
    left_on="Genes",
    right_on="HGNC ",
    how="left"
)

# Optional: drop the extra 'HGNC' column if not needed
merged_df.drop(columns=["HGNC "], inplace=True)

# Save the result (optional)
merged_df.to_excel("ABPP_with_Kinase_Classification.xlsx", index=False)

