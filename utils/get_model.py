import pathlib

from keras.models import model_from_json

PATH = pathlib.Path(__file__).parent
MODEL_PATH = PATH.joinpath("../models").resolve()


def get_model(ticker):

    # load json and create model
    json_file = open(MODEL_PATH.joinpath("regressor.json"), "r")
    loaded_model_json = json_file.read()
    json_file.close()

    regressor = model_from_json(loaded_model_json)
    # load weights into new model

    regressor.load_weights(MODEL_PATH.joinpath(ticker + ".h5"))

    return regressor
