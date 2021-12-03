import pathlib

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import requests
import yfinance as yf
from dash.dependencies import Input, Output

from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

data = yf.download(  # or pdr.get_data_yahoo(...
    # tickers  or string as well
    tickers="AUD=X CAD=X EUR=X INR=X USD",
    # use "period" instead of start/end
    # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    # (optional, default is '1mo')
    period="1d",
    # fetch data by interval (including intraday if period < 60 days)
    # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    # (optional, default is '1d')
    interval="1m",
)

# data = data.dropna()
data = data.fillna(method="ffill").reset_index()

data = data.loc[:, ["Datetime", "Close"]].tail(2)
