# app/db.py

from databases import Database
from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, Boolean
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import registry

import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@localhost:3306/openwebui"
)

database = Database(DATABASE_URL)

mapper_registry = registry()
Base = mapper_registry.generate_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=320), unique=True, nullable=False, index=True)
    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

