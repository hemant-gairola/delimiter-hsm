# coding: utf-8
#
# Copyright (c) 2023 by Delphix. All rights reserved.
#
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from src.databases.database import Base

Base = declarative_base()
metadata = Base.metadata


class DataSet(Base):
    __tablename__ = "data_set"

    id = Column(Integer, primary_key=True)
    data = Column(Text, nullable=False)
