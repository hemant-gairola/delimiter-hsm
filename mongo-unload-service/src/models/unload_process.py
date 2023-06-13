# coding: utf-8
#
# Copyright (c) 2023 by Delphix. All rights reserved.
#
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UnloadProcess(Base):
    __tablename__ = "unload_process"

    id = Column(Integer, primary_key=True)
    data = Column(Text, nullable=False)
