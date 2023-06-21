#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

from sqlalchemy.orm import Session


class UnloadService:
    def create(self):
        self.start_unload()

    def start_unload(self, data_info, unload_data, table_row_count, db: Session):
        # Add entry in source_data
        # Add entry in source_data_info
        self.createInitialSourceDataInfo(listOfDataInfo, unloadData, tableRowCountMap)
