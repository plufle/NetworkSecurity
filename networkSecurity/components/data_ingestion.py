import os 
import sys 
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import pymongo
import pandas as pd
import numpy as np 
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()


MONGO_DB_URL = os.environ.get("MONGO_DB_URL")


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info("Data ingestion started")
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        try:
            logging.info("Exporting collection as dataframe")
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            dataframe = pd.DataFrame(list(collection.find()))
            logging.info("Successfully exported collection as dataframe")

            if "_id" in dataframe.columns.to_list():
                dataframe.drop("_id",axis=1,inplace=True)
            
            dataframe.replace({"na":np.nan},inplace=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            logging.info("Exporting data into feature store")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(os.path.dirname(feature_store_file_path),exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            logging.info("Successfully exported data into feature store")
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            logging.info("Splitting data as train test")
            train_set, test_set = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)

            dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_set.to_csv(self.data_ingestion_config.train_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)
            logging.info("Successfully split data as train test")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    


    
