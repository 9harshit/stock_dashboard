import pathlib

import numpy as np
import pandas as pd
import joblib

from utils import data_download, get_model

PATH = pathlib.Path(__file__).parent
MODEL_PATH = PATH.joinpath("../models").resolve()


def get_prediction(ticker):

    data = data_download(ticker, "1m").tail(10)

    datetime = pd.to_datetime(data.Datetime)

    data = data.drop(["Datetime"], axis=1)

    X_test = []

    for i in range(10, (data.shape[0])):
        X_test.append(data[i - 10 : i])

    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 5))

    model = get_model(ticker)

    sc = joblib.load(MODEL_PATH.joinpath("scaler_{}.pkl").format(ticker))

    prediction = model.predict(X_test)
    prediction = pd.DataFrame(sc.inverse_transform(prediction)).rename(
        columns={"0": "Price"}
    )
    prediction["Type"] = "Predicted"

    prediction = prediction.append(data.Close)

    prediction.loc[len(prediction) - len(data) :, "Type"] = "Actual"
    prediction["Datetime"] = datetime

    prediction.loc[-1, "Datetime"] = prediction.loc[-2, "Datetime"] + pd.Timedelta(
        1, "m"
    )

    return prediction
