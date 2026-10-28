# FOR TRANSFORMING THE DATA  ( WE DO FEATURE ENGINEERING AND DATA CLEANING )
import sys 
from dataclasses import dataclass

import numpy as np 
import pandas as pd 
from sklearn.compose import ColumnTransformer
from src.utils import save_object


from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

@dataclass 
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join(
    'artifacts', 'preprocessor.pkl'
)

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_columns=["writing_score","reading_score"]
            categorial_columns=[
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())

                ])
            # here in this num_pipeline, we are handling missing value and performing standard scaler 

            
            cat_pipeline=Pipeline(

                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("One_hot_encoder",OneHotEncoder())
                ]
            )# this is performing the onehot encoding and standard scaling 


            logging.info("Numerical columns encoding completed")
            logging.info("Categorial columns encoding completed")

            preprocessor=ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ("cat_pipelines",cat_pipeline,categorial_columns),
                ]
            )# this is the combination of numerical and categorial pipeline 

            return preprocessor

        except Exception as e: 
            raise CustomException(e,sys)
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info("obtaning preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name = "math_score"
            numerical_columns=["writing_score","reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name])
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name])
            target_feature_test_df=test_df[target_column_name]

            logging.info("Applying preprocessing object on training dataframes and testing dataframe")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df) # for fit_transform : Learn mean and standard deviation, then transform
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df) # for transform :   Reuse the same mean and standard deviation

            train_arr = np.c_[
                input_feature_train_arr,np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                            input_feature_test_arr,np.array(target_feature_test_df)
                        ]
            logging.info(f"savedpreprocessing object.")

            
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        
        except Exception as e:
            raise CustomException(e,sys) 