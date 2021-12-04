import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app, server

# Connect to your app pages
from apps import currency_tracker, error, price_predictor

layout = html.Div(
    [
        html.H1("404 Error", style={"textAlign": "center"}),
    ]
)
