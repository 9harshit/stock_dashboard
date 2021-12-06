import pathlib
from datetime import datetime

import dash_core_components as dcc
import dash_html_components as html
import geopandas as gpd
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

from app import app
from utils import data_download

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
        dcc.Loading(
            id="loading-1",
            children=[html.Div([html.Div(id="loading-output-1")])],
            type="graph",
            fullscreen=True,
        ),
        html.Label(id="label", children=[]),
        html.Div(
            [dcc.Graph(id="map", figure={}), dcc.Graph(id="chart", figure={})],
            style={
                "display": "flex",
                "width": "100%",
                "flex-direction": "row",
                "justify-content": "center",
            },
        ),
        dcc.Interval(
            id="interval-component", interval=300000, n_intervals=0  # in milliseconds
        ),
    ]
)


@app.callback(
    [
        Output(component_id="map", component_property="figure"),
        Output(component_id="chart", component_property="figure"),
        Output("loading-output-1", "children"),
        Output("label", "children"),
    ],
    [Input("interval-component", "n_intervals")],
)
def display_value(n_intervals):

    df = pd.DataFrame(columns=["Country", "Currency", "name"], index=range(0, 100))

    map = gpd.read_file(DATA_PATH.joinpath("countries.geojson"))
    map = map[["name", "iso_a3"]]
    map = map[map["name"].isin(COUNTRY)]

    bar_df = pd.DataFrame()

    for i, ticker in enumerate(
        ["AUD=X", "CAD=X", "EUR=X", "INR=X", "USD", "GBP=X", "RUB=X", "CNY=X"], 0
    ):

        data = data_download.data_download(ticker, "5m").iloc[::-1]

        data["Country"] = ticker.split("=")[0]

        data = data.loc[:, ["Datetime", "Close", "Country"]].tail(10)

        df.loc[i]["Country"] = ticker.split("=")[0]
        df.loc[i]["Currency"] = (
            "Down" if data.iloc[-2]["Close"] > data.iloc[-1]["Close"] else "Up"
        )
        df.loc[i]["name"] = COUNTRY[i]

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

    return (
        fig1,
        fig2,
        {},
        "Last Updated on: " + datetime.now().strftime("%m/%d/%Y,%H:%M:%S"),
    )
