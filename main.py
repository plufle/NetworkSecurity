from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from networksecurity.logging.logger import logging


import os
import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        logging.info("Data ingestion config created")
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion() 
        print("The Data Ingestion Artifact is :",data_ingestion_artifact)
        logging.info("Data ingestion completed")
    except Exception as e:
        logging.error("Data ingestion failed")
        raise NetworkSecurityException(e, sys) 
 