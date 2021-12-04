import yfinance as yf


def data_download(ticker: str, interval: str):
    """Download data for a ticker from yahoo finance"""

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
        interval=interval,
    )

    data = data.fillna(method="ffill").reset_index()
    data = data.drop_duplicates()

    return data
