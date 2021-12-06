#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 11:02:29 2021

@author: harshit
"""

# Recurrent Neural Network

# Part 1 - Data Preprocessing

import pathlib

import matplotlib.pyplot as plt

# Importing the libraries
import numpy as np
import pandas as pd
import yfinance as yf
from keras.layers import LSTM, Bidirectional, Dense, Dropout

# Importing the Keras libraries and packages
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler

from utils.data_download import data_download

import joblib

PATH = pathlib.Path('__file__').parent
MODEL_PATH = PATH.joinpath("../models").resolve()


def create_model(ticker: str):
    # Importing the training set
    dataset_train = data_download(ticker, "1m").loc[::-1, ["Datetime", "Close"]]

    dataset_train = dataset_train.dropna()
    training_set = dataset_train.iloc[:, 1:].values
    # Feature Scaling

    sc = MinMaxScaler(feature_range=(0, 1))
    training_set_scaled = sc.fit_transform(training_set)

    # Creating a data structure with 60 DAYsteps and 1 output
    X_train = []
    y_train = []
    for i in range(10, (training_set_scaled.shape[0])):
        X_train.append(training_set_scaled[i - 10 : i])
        y_train.append(training_set_scaled[i])
    X_train, y_train = np.array(X_train), np.array(y_train)

    # Reshaping
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    # Part 2 - Building the RNN

    # Initialising the RNN
    regressor = Sequential()

    # Adding the first LSTM layer and some Dropout regularisation
    regressor.add(
        Bidirectional(
            LSTM(75, return_sequences=True), input_shape=(X_train.shape[1], 1)
        )
    )
    regressor.add(Dropout(0.2))

    # Adding a second LSTM layer and some Dropout regularisation
    regressor.add(Bidirectional((LSTM(75, return_sequences=True))))
    regressor.add(Dropout(0.2))

    # Adding a third LSTM layer and some Dropout regularisation
    regressor.add(Bidirectional((LSTM(75, return_sequences=True))))
    regressor.add(Dropout(0.2))

    # Adding a fourth LSTM layer and some Dropout regularisation
    regressor.add(Bidirectional(LSTM(units=75)))
    regressor.add(Dropout(0.2))

    # Adding the output layer
    regressor.add(Dense(units=1))

    # Compiling the RNN
    regressor.compile(optimizer="adam", loss="mean_squared_error")

    # Fitting the RNN to the Training set
    regressor.fit(X_train, y_train, epochs=30, batch_size=32)

    joblib.dump(sc, "{}.pkl".format(ticker))

    model_json = regressor.to_json()

    with open(MODEL_PATH.joinpath("{}.json".format(ticker)), "w") as json_file:
        json_file.write(model_json)

    regressor.save(MODEL_PATH.joinpath("{}.h5".format(ticker)))

    return True


create_model("SBIN.NS")
