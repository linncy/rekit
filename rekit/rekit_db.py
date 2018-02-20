from sqlalchemy import *
from sqlalchemy.engine.url import URL
import os

def create_db(basedir='./db',dbname='db.sqlite'):
	if not os.path.exists(basedir):
		print('Create the directory: ' + basedir)
		call(['mkdir',basedir])
	sqlite_db={'drivername':'sqlite','database':os.path.join(basedir, dbname)}
	db_url=URL(**sqlite_db)
	engine=create_engine(db_url)
	metadata=MetaData(engine)
	table_info=Table('info',metadata,Column('info_id',Integer,primary_key=True,autoincrement=True,unique=True,nullable=False),Column('info_name',String),Column('info_value',String))
	table_stu=Table('stu',metadata,Column('stu_uid',Integer,primary_key=True,autoincrement=True,unique=True,nullable=False),Column('stuid',String,nullable=False,unique=True),Column('stu_name',String),Column('stu_numofhw',Integer),Column('stu_finalhwgrade',REAL))
	table_hw=Table('hw',metadata,Column('hw_id',Integer,primary_key=True,autoincrement=True,unique=True,nullable=False),Column('hw_available',BOOLEAN,nullable=False),Column('hw_due',String,nullable=False),Column('hw_distributions',Integer),Column('hw_collections',Integer),Column('hw_higrade',REAL),Column('hw_lograde',REAL),Column('hw_avgrade',REAL))
	table_score=Table('score',metadata,Column('hw_id',Integer,ForeignKey("hw.hw_id"),nullable=False),Column('stu_uid',Integer,ForeignKey("stu.stu_uid"),nullable=False),Column('stuid',String,ForeignKey("stu.stuid"),nullable=False),Column('score',REAL,nullable=False))
	table_token=Table('token',metadata,Column('hw_id',Integer,ForeignKey("hw.hw_id"),nullable=False),Column('stu_uid',Integer,ForeignKey("stu.stu_uid"),nullable=False),Column('stuid',String,ForeignKey("stu.stuid"),nullable=False),Column('token',String,nullable=False))
	table_log=Table('log',metadata,Column('log_id',Integer,primary_key=True,autoincrement=True,unique=True,nullable=False),Column('time',String,nullable=False),Column('stu_uid',Integer,ForeignKey("stu.stu_uid"),nullable=False),Column('log',String))
	metadata.create_all()
	return db_url

def eclassdict2db(eclassdict,db_url):
	return 1