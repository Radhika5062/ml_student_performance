import os
import sys
import numpy as np
import pandas as pd
from exception import CustomException
from logger import logging
import dill
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok= True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)

def evaluate_models(X_train, y_train, X_test, y_test, models, params):
    try:
        report = {}

        for i in range(len(models)):
            logging.info(f"Models = {models}")
            model = list(models.values())[i]
            logging.info(f"Model = {model}")
            logging.info(f"Model = {list(models.keys())[i]}")
            param = params[list(models.keys())[i]]
            logging.info(f"Param = {param}")

            logging.info(f"Currently evaluating {model}")
            logging.info(f"Current Params are {param}")

            gs = GridSearchCV(model, param, cv = 3)
            gs.fit(X_train, y_train)

            logging.info(f'Best params are {gs.best_params_}')

            model.set_params(**gs.best_params_)

            model.fit(X_train, y_train) # Training
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score
            logging.info(f'report = {report}')
        return report
    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise(e, sys)