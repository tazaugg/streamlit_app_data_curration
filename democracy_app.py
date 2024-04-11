import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
st.set_option('deprecation.showPyplotGlobalUse', False)
# Load the dataset
url = "https://github.com/tazaugg/data_curation/raw/main/merged.csv"
df = pd.read_csv(url)
df_numeric = df.drop(columns=["Country", "Democracy classification"])
df_numeric = df_numeric.apply(pd.to_numeric, errors='coerce')

grouped_data = df_numeric.groupby(df["Democracy classification"]).mean()

averages = df_numeric.groupby(df["Democracy classification"]).mean().reset_index()
averages["Country"] = "Average " + averages["Democracy classification"]

df = pd.concat([df, averages], ignore_index=True, sort=False)
st.title("Democracy Index Dataset Explorer")
st.subheader("Filtered Dataset")
selected_columns = st.multiselect(
    "Select columns to display", df.columns.tolist()
)

selected_classifications = st.multiselect(
    "Select Democracy Classification", df["Democracy classification"].unique()
)

filtered_df = df[df["Democracy classification"].isin(selected_classifications)][selected_columns]

sort_by = st.multiselect(
    "Select column to sort by", selected_columns
)


if sort_by:
    for column in sort_by:
        if column == "Country":
            filtered_df = filtered_df.sort_values(by=column)
        else:
            filtered_df = filtered_df.sort_values(by=[column])
filtered_df = filtered_df.rename(columns={"Country": "Country                                               "})

st.write(filtered_df)

st.subheader("Bar Charts")

selected_countries = st.multiselect(
    "Select countries", df["Country"].unique()
)

columns_to_compare = st.multiselect(
    "Select columns to compare", df.columns.tolist()
)

filtered_data_for_countries = df[df["Country"].isin(selected_countries)]

if selected_countries and columns_to_compare:
    for column in columns_to_compare:
        st.subheader(f"Bar Chart for {column}")
        st.bar_chart(filtered_data_for_countries.set_index("Country")[column])


st.subheader("Boxplots by Democracy Classification")

columns_for_boxplot = st.multiselect(
    "Select columns for boxplot", df_numeric.columns.tolist()
)

if columns_for_boxplot:
    for column in columns_for_boxplot:
        plt.figure(figsize=(10, 6))
        sns.boxplot(x="Democracy classification", y=column, data=df)
        plt.title(f"Boxplot of {column} by Democracy Classification")
        plt.xlabel("Democracy classification")
        plt.ylabel(column)
        st.pyplot()