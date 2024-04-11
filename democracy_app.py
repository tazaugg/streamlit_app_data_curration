import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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

st.set_page_config(layout="wide")
title = """
    <div style="display: flex; justify-content: center; align-items: center;">
        <h1>Democracy Index Dataset Explorer</h1>
    </div>
"""

st.markdown(title, unsafe_allow_html=True)

cols = st.columns([1, 3, 1])

text = 'This app is designed to help you explore data that contains information about Countries and various metrics of success compared to their level of Democracy'
text2 = '\n\nIf you would like to learn more about this data and how it was collected I would encourage you to loop through my'
text3 = ' [repo](https://github.com/tazaugg/data_curation) as well as explore my [data collection blog](https://tazaugg.github.io/blog_practice/2024/03/30/democracy-sucess.html)'
text4 = '\n\nHave fun exploring the data below!!'

cols[1].markdown(text+text2+text3+text4, unsafe_allow_html=True)








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
        ascending = st.radio(f"Sort {column}:", ["High to Low", "Low to High"], key=column)
        if ascending == "High to Low":
            filtered_df = filtered_df.sort_values(by=[column], ascending=False)
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