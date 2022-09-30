import os
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ARRAY)
import uuid

from databases import Database

DATABASE_URI = 'postgresql://postgres:1516@localhost/user_db'#os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

users = Table(
    'user',
    metadata,
    
    Column('email', String(100),nullable=False),
    Column('username', String(100), unique=True,nullable=False),
    Column('password', String(100),nullable=False),
    Column('id',Integer, primary_key=True),
)

database = Database(DATABASE_URI)





