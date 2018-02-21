from sqlalchemy import Column, Integer, String, REAL, BOOLEAN
from sqlalchemy.engine.url import URL
from sqlalchemy import engine
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
from . import models
from subprocess import call
from sqlalchemy import MetaData, Table, Column, ForeignKey

def create_db(basedir='./db',dbname='db.sqlite'):
	if not os.path.exists(basedir):
		print('Create the directory: ' + basedir)
		call(['mkdir',basedir])
	sqlite_db={'drivername':'sqlite','database':os.path.join(basedir, dbname)}
	db_url=URL(**sqlite_db)
	engine=create_engine(db_url)
	metadata=MetaData(engine)
	table_info=Table('info',metadata,
		Column('info_id',Integer,primary_key=True,unique=True,nullable=False),
		Column('info_name',String),
		Column('info_value',String),
		sqlite_autoincrement=True)
	table_stu=Table('stu',metadata,
		Column('stu_uid',Integer,primary_key=True,unique=True,nullable=False),
		Column('stuid',String,nullable=False,unique=True),Column('stu_name',String),
		Column('stu_numofhw',Integer),Column('stu_finalhwgrade',REAL),
		sqlite_autoincrement=True)
	table_hw=Table('hw',metadata,
		Column('hw_id',String,primary_key=True,unique=True,nullable=False),
		Column('hw_available',BOOLEAN,nullable=False),
		Column('hw_due',String,nullable=False),
		Column('hw_distributions',Integer),
		Column('hw_collections',Integer),
		Column('hw_higrade',REAL),
		Column('hw_lograde',REAL),
		Column('hw_avgrade',REAL))
	table_score=Table('score',metadata,
		Column('score_id',Integer,primary_key=True,unique=True,nullable=False),
		Column('hw_id',String,ForeignKey("hw.hw_id"),nullable=False),
		Column('stu_uid',Integer,ForeignKey("stu.stu_uid"),nullable=False),
		Column('stuid',String,ForeignKey("stu.stuid"),nullable=False),
		Column('score',REAL,nullable=False),
		sqlite_autoincrement=True)
	table_token=Table('token',metadata,
		Column('token_id',Integer,primary_key=True,unique=True,nullable=False),
		Column('hw_id',String,ForeignKey("hw.hw_id"),nullable=False),
		Column('stu_uid',Integer,ForeignKey("stu.stu_uid"),nullable=False),
		Column('stuid',String,ForeignKey("stu.stuid"),nullable=False),
		Column('token',String,nullable=False),
		sqlite_autoincrement=True)
	table_log=Table('log',metadata,
		Column('log_id',Integer,primary_key=True,unique=True,nullable=False),
		Column('time',String,nullable=False),
		Column('stu_uid',Integer,ForeignKey("stu.stu_uid"),nullable=False),
		Column('log',String),
		sqlite_autoincrement=True)
	metadata.create_all()
	return db_url

def eclassdict2db(eclassdict,db_url):
	engine = create_engine(db_url)
	Session=sessionmaker(bind=engine)
	session=Session()
	for key in ['course','term','classnumber','numofstu']:
		info=models.info(info_name=key,info_value=eclassdict[key])
		session.add(info)
	for i in range(eclassdict['numofstu']):
		stu=models.stu(stuid=eclassdict['student'][str(i)]['stuid'],stu_name=eclassdict['student'][str(i)]['name'])
		session.add(stu)
	session.commit()
	session.close()
