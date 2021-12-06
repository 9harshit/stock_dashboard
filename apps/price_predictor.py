import pathlib
from datetime import datetime

import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

from app import app
from utils.get_prediction import get_prediction

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
        dcc.Loading(
            id="loading-2",
            children=[html.Div([html.Div(id="loading-2")])],
            type="graph",
            fullscreen=True,
        ),
        html.Div(
            dcc.RadioItems(
                id="input-radio-button",
                options=[
                    {"label": "Apple", "value": "AAPL"},
                    {"label": "SBI", "value": "SBIN.NS"},
                ],
                value="AAPL",
                labelStyle={"display": "inline-block"},
            )
        ),
        html.Div(
            [
                dcc.Graph(id="price_chart", figure={}),
                dt.DataTable(id="table"),
            ],
            style={
                "display": "flex",
                "flex-direction": "row",
                "justify-content": "center",
                "width": "100%",
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
        Output("loading-2", "children"),
    ],
    [Input("interval-component", "n_intervals"), Input("input-radio-button", "value")],
)
def display_value(n_intervals, radio_button_value):

    # data = pd.read_csv(DATA_PATH.joinpath("apple_5_test.csv"))
    print(radio_button_value)
    data = get_prediction(radio_button_value)
    print(data)
    fig = px.line(data, x="Datetime", y="Price", color="Type")

    return (
        fig,
        data.to_dict(orient="records"),
        [{"name": col, "id": col} for col in data.columns],
        "Last Updated on: " + datetime.now().strftime("%m/%d/%Y,%H:%M:%S"),
        {},
    )
