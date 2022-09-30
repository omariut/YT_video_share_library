import os

from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ARRAY)

from databases import Database

DATABASE_URI = 'postgresql://postgres:1516@localhost/video_db'#os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

videos = Table(
    'video',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('code', String(50), unique=True),
    Column('username', String(50)),
    Column('total_likes', Integer),
    Column('total_dislikes', Integer),
    Column('total_comments', Integer),
    Column('total_views', Integer),


)

database = Database(DATABASE_URI)