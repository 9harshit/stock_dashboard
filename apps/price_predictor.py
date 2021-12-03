import pathlib
from time import sleep

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import geopandas as gpd
import plotly.express as px
import requests
import yfinance as yf
from dash.dependencies import Input, Output, State
import time

from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
COUNTRY = [
    "Australia",
    "Canada",
    "Germany",
    "India",
    "United States",
    "United Kingdom",
    "Russia",
    "China",
]
pd.options.plotting.backend = "plotly"


df = pd.DataFrame(columns=["Country", "Currency", "name"], index=range(0, 100))

map = gpd.read_file(DATA_PATH.joinpath("countries.geojson"))
map = map[["name", "iso_a3"]]
map = map[map["name"].isin(COUNTRY)]

bar_df = pd.DataFrame()

for i, ticker in enumerate(
    ["AUD=X", "CAD=X", "EUR=X", "INR=X", "USD", "GBP=X", "RUB=X", "CNY=X"], 0
):

    data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers  or string as well
        tickers=ticker,
        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period="1d",
        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval="1m",
    )
    data = data.fillna(method="ffill").reset_index()

    data = data.loc[:, ["Datetime", "Close"]].tail(10)

    df.loc[i]["Country"] = ticker.split("=")[0]
    df.loc[i]["Currency"] = 0 if data.iloc[-2]["Close"] > data.iloc[-1]["Close"] else 1
    df.loc[i]["name"] = COUNTRY[i]

    data = data.rename(columns={"Close": COUNTRY[i]})

    if i == 0:
        bar_df = pd.concat([bar_df, data], axis=1)
    else:
        bar_df = pd.concat([bar_df, data[COUNTRY[i]]], axis=1)


map = map.merge(df, on="name")

layout = html.Div(
    [
        html.H1("Currency Tracker", style={"textAlign": "center"}),
        html.Button("Refresh", id="submit-val", n_clicks=0),
        dcc.Graph(id="map", figure={}),
        dcc.Graph(id="chart", figure={}),
    ]
)
bar_df = bar_df.drop_duplicates()
bar_df = bar_df.fillna(method="ffill")
bar_df = bar_df.tail(10)
print(bar_df)


@app.callback(
    [
        Output(component_id="map", component_property="figure"),
        Output(component_id="chart", component_property="figure"),
    ],
    Input("submit-val", "n_clicks"),
)
def display_value(n_clicks):

    fig1 = px.choropleth(map, locations=map.iso_a3, color="Currency", hover_name="name")
    print(n_clicks)
    # return px.bar(df, x="Country", y="Currency")

    fig2 = px.line(bar_df, x=bar_df.Datetime, y="Australia", title="Currency Tracker")

    return fig1, fig2
