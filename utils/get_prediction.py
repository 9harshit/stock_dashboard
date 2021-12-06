import pathlib

import joblib
import numpy as np
import pandas as pd

from utils.data_download import data_download
from utils.get_model import get_model

PATH = pathlib.Path(__file__).parent
MODEL_PATH = PATH.joinpath("../models").resolve()


def get_prediction(ticker):

    data = (
        data_download(ticker, "1m")
        .loc[::-1, ["Datetime", "Close"]]
        .tail(20)
        .reset_index(drop=True)
    )

    datetime = pd.to_datetime(data.loc[10:, "Datetime"]).reset_index(drop=True)

    datetime = datetime.iloc[::-1].reset_index(drop=True)

    data = data.drop(["Datetime"], axis=1)

    X_test = []

    for i in range(10, (data.shape[0])):
        X_test.append(data[i - 10 : i])

    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    model = get_model(ticker)

    sc = joblib.load(MODEL_PATH.joinpath("{}.pkl".format(ticker)))

    prediction = model.predict(X_test)

    prediction = pd.DataFrame(sc.inverse_transform(prediction)).rename(
        columns={0: "Price"}
    )
    prediction["Type"] = "Predicted"

    data["Type"] = "Actual"

    prediction = (
        data.reset_index(drop=True)
        .rename(columns={"Close": "Price"})
        .tail(10)
        .append(prediction)
        .reset_index(drop=True)
    )

    prediction["Datetime"] = datetime

    datetime.index += 9
    print(datetime)
    prediction.loc[10:19, "Datetime"] = datetime

    prediction.loc[len(prediction) - 1, "Datetime"] = prediction.loc[
        len(prediction) - 2, "Datetime"
    ] + pd.Timedelta(1, "m")

    return prediction
