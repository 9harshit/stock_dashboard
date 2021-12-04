import pathlib

import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd
import plotly.express as px
import yfinance as yf
from dash.dependencies import Input, Output
from app import app
from datetime import datetime

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()


layout = html.Div(
    [
        html.H1("Stock Price Prediction", style={"textAlign": "center"}),
        # dcc.Loading(
        #     id="loading-1",
        #     children=[html.Div([html.Div(id="loading-output-1")])],
        #     type="circle",
        # ),
        html.Label(id="update_label", children=[]),
        html.Div(
            [
                dcc.Graph(id="price_chart", figure={}),
                dt.DataTable(id="table"),
            ],
            style={
                "display": "flex",
                "flex-direction": "row",
                "justify-content": "center",
            },
        ),
        dcc.Interval(
            id="interval-component", interval=600000, n_intervals=0  # in milliseconds
        ),
    ]
)


@app.callback(
    [
        Output(component_id="price_chart", component_property="figure"),
        Output(component_id="table", component_property="data"),
        Output(component_id="table", component_property="columns"),
        Output("update_label", "children"),
    ],
    Input("interval-component", "n_intervals"),
)
def display_value(n_intervals):

    # fig2 = px.line(bar_df, x="Datetime", y="Close", color="Country")
    data = pd.read_csv(DATA_PATH.joinpath("apple_5_test.csv"))
    return (
        {},
        data.to_dict(orient="records"),
        [{"name": col, "id": col} for col in data.columns],
        "Last Updated on: " + datetime.now().strftime("%m/%d/%Y,%H:%M:%S"),
    )
