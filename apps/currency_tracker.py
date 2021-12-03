import pathlib

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import geopandas as gpd
import plotly.express as px
import yfinance as yf
from dash.dependencies import Input, Output
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


layout = html.Div(
    [
        html.H1("Currency Tracker", style={"textAlign": "center"}),
        dcc.Graph(id="map", figure={}),
        dcc.Graph(id="chart", figure={}),
        dcc.Interval(
            id="interval-component", interval=60000, n_intervals=0  # in milliseconds
        ),
    ]
)


@app.callback(
    [
        Output(component_id="map", component_property="figure"),
        Output(component_id="chart", component_property="figure"),
    ],
    Input("interval-component", "n_intervals"),
)
def display_value(n_intervals):

    df = pd.DataFrame(columns=["Country", "Currency", "name"], index=range(0, 100))

    map = gpd.read_file(DATA_PATH.joinpath("countries.geojson"))
    map = map[["name", "iso_a3"]]
    map = map[map["name"].isin(COUNTRY)]

    bar_df = pd.DataFrame()
    print("erer")

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
        data = data.drop_duplicates()

        data["Country"] = ticker

        data = data.loc[:, ["Datetime", "Close", "Country"]].tail(10)

        df.loc[i]["Country"] = ticker.split("=")[0]
        df.loc[i]["Currency"] = (
            0 if data.iloc[-2]["Close"] > data.iloc[-1]["Close"] else 1
        )
        df.loc[i]["name"] = ticker.split("=")[0]

        bar_df = bar_df.append(data.tail(10))
        bar_df = bar_df.drop_duplicates()
        bar_df = bar_df.fillna(method="ffill")

    map = map.merge(df, on="name")

    # if i == 0:
    #     bar_df = pd.concat([bar_df, data], axis=1)
    # else:
    #     bar_df = pd.concat([bar_df, data[COUNTRY[i]]], axis=1)

    print("auto update...")

    fig1 = px.choropleth(map, locations=map.iso_a3, color="Currency", hover_name="name")
    # return px.bar(df, x="Country", y="Currency")

    # fig2 = px.line(bar_df, x=bar_df.Datetime, y="Australia", title="Currency Tracker")

    fig2 = px.line(bar_df, x="Datetime", y="Close", color="Country")

    return fig1, fig2
