# i want to create a streamlit app to draw a graph of the usage by interpreting the data from supabase

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import json
import altair as alt


def fetch_all_rows(table_name, chunk_size=1000):
    # load .env file
    load_dotenv()

    # key to know the local of the code being run
    production = os.environ.get("PRODUCTION")

    # Supabase configuration
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    offset = 0
    all_data = []

    while True:
        # Fetch a chunk of data
        response = (
            supabase.table(table_name)
            .select("*")
            .range(offset, offset + chunk_size - 1)
            .execute()
        )
        data_chunk = response.data

        # Break the loop if no more data is returned
        if not data_chunk:
            break

        # Append the chunk to the all_data list
        all_data.extend(data_chunk)

        # Update the offset
        offset += chunk_size

    return all_data


def get_data():
    # get the data from supabase

    # data = supabase.table("ide_uploads").select("*").execute()
    data = fetch_all_rows("ide_uploads")
    return data


st.title("MGFHUB IDE Usage")

data = get_data()
df = pd.DataFrame(data)

# create a column that gets the year and month of the created_at column
df["created_at"] = pd.to_datetime(df["created_at"])
df["year"] = df["created_at"].dt.year
df["month"] = df["created_at"].dt.month
df["yearmonth"] = df["year"].astype(str) + "-" + df["month"].astype(str)


# get a frequency count of the unidade by yearmonth
df_unidades = df.groupby(["yearmonth", "unidade"]).size().reset_index(name="count")

# make each unidade a column and fill the NaN with 0
df_unidades = df_unidades.pivot(
    index="unidade", columns="yearmonth", values="count"
).fillna(0)
# make a new row with the total of each row
df_unidades.loc["Total"] = df_unidades.sum()
# make a new column with the total of each column
df_unidades["Total"] = df_unidades.sum(axis=1)
st.write(df_unidades)

# get frequency count of yearmonth
df_yearmonth = df.groupby(["yearmonth"]).size().reset_index(name="count")

# create a bar chart from the frequency count of yearmonth
bar_chart = (
    alt.Chart(df_yearmonth)
    .mark_bar()
    .encode(x="yearmonth", y="count")
    .properties(width=600, height=300)
)
st.write(bar_chart)

# Display the DataFrame in Streamlit
# st.write(df)
