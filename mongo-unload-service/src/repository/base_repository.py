#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

import json

from sqlalchemy.orm import Session
from src.databases.database import SessionLocal
from src.models.connector import Connector
from src.models.data_set import DataSet
from src.models.source_data import SourceData
from src.models.unload_process import UnloadProcess


class BaseRepository:
    def get_db(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def createTable(self):
        pass

    def createIndex(self):
        pass

    def listAll(self):
        pass

    def save(self, data: dict, db: Session):
        """
        This will insert the data into data-set table
        """
        db_data_info_data = json.dumps(data)
        print(f"Hemant 1 : {data}")
        db_data_info = DataSet(data=db_data_info_data)
        print(f"Hemant 2 : {db_data_info}")
        db.add(db_data_info)
        db.commit()
        db.refresh(db_data_info)
        return db_data_info

    def save_data_into_connector(self, data: dict, db: Session):
        """
        This will insert the data into data-set table
        """
        print(f"Hemant 1 : {data}")
        response = {
            "jdbcUrl": data["jdbc_url"],
            "user": data["user"],
            "password": data["password"],
            "connectionProperties": None,
            "restoreSensitiveFields": False,
        }

        db_connector_info_data = json.dumps(response)
        db_connector_info = Connector(data=db_connector_info_data)
        print(f"Hemant 2 : {db_connector_info}")
        db.add(db_connector_info)
        db.commit()
        db.refresh(db_connector_info)
        return db_connector_info

    def save_into_source_data(
        self,
        source_key,
        unload_data: dict,
        unloadSplitCount,
        table_row_count_map,
        db: Session,
    ):
        response = {
            "executionId": unload_data["execution_id"],
            "sourceKey": source_key,
            "unloadSplitCount": unloadSplitCount,
            "totalNumberOfRows": table_row_count_map,
            "maskingSplitCount": None,
        }
        print(f"For Hemant 100 : {json.dumps(response)}")
        source_data_info = SourceData(data=json.dumps(response))
        db.add(source_data_info)
        db.commit()
        db.refresh(source_data_info)
        return source_data_info

    def save_into_unload_process_data_info(
        self, source_key, execution_id, split_file_name, db
    ):
        response = {
            "executionId": execution_id,
            "sourceKey": source_key,
            "unloadFilePath": split_file_name,
            "rowsUnloaded": 0,
            "status": "SUCCEEDED",
            "error": None,
        }
        unload_process_data_info = UnloadProcess(data=json.dumps(response))
        db.add(unload_process_data_info)
        db.commit()
        db.refresh(unload_process_data_info)
        return unload_process_data_info

    def update(self):
        pass

    def exists(self):
        pass

    def delete(self):
        pass

    def deleteIfExists(self):
        pass

    def getById(self, db: Session, id: int):
        data = db.query(DataSet).filter(DataSet.id == id).first()
        return data

    def getByIdsourceData(self, db: Session, id: int):
        data = db.query(SourceData).filter(DataSet.id == id).first()
        return data

    def getByData(self):
        pass

    def getByDataAndId(self):
        pass

    def getOptional(self):
        pass

    def list(self):
        pass

    def getRawJsonById(self, id):
        pass
