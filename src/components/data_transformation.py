import sys
from dataclasses import dataclass 
import numpy as np
import pandas as pd 
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from exception import CustomException 
from logger import logging
from utils import save_object
import os

@dataclass
class DataTransformationConfig:
    preprocessor_object_file_path = os.path.join('artifact', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def get_data_tranformer_object(self):
        try:
            numerical_columns = ["writing score", "reading score"]
            categorical_columns = ['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course']

            num_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy = "median")),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            cat_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy = "most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info("Columns Transformations initialized in Pipeline")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            logging.info("Column transformations applied")

            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info('Read train and test data complete')

            logging.info('Obtaining preprocessing object')

            preprocessing_obj = self.get_data_tranformer_object()

            target_column_name = "math score"
            numerical_columns = ["writing score", "reading score"]

            logging.info(f"train_df columns are = {train_df.columns}")

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis = 1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns = [target_column_name], axis = 1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying the processing object on the training dataframe and testing dataframe")

            logging.info(f"input_feature_train_df columns are = {input_feature_train_df.columns}")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]

            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info('Saving preprocessing object')

            save_object(self.data_transformation_config.preprocessor_object_file_path, obj = preprocessing_obj)

            return (
                train_arr, test_arr, self.data_transformation_config.preprocessor_object_file_path
            )
        except Exception as e:
            raise CustomException(e, sys)








