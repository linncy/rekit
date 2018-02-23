from sqlalchemy import Column, Integer, String, REAL, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
import binascii, os
Base = declarative_base()

class info(Base):
	__tablename__='info'
	info_id=Column('info_id',Integer,primary_key=True,unique=True,nullable=False)
	info_name=Column('info_name',String,unique=True)
	info_value=Column('info_value',String)

class stu(Base):
	__tablename__='stu'
	stu_uid=Column('stu_uid',Integer,primary_key=True,unique=True,nullable=False)
	stuid=Column('stuid',String,nullable=False,unique=True)
	stu_name=Column('stu_name',String)
	stu_email=Column('stu_email',String)
	stu_numofhw=Column('stu_numofhw',Integer)
	stu_finalhwgrade=Column('stu_finalhwgrade',REAL)

class hw(Base):
	__tablename__='hw'
	hw_id=Column('hw_id',Integer,primary_key=True,unique=True,nullable=False)
	hw_available=Column('hw_available',BOOLEAN,nullable=False)
	hw_due=Column('hw_due',String,nullable=False)
	hw_distributions=Column('hw_distributions',Integer)
	hw_collections=Column('hw_collections',Integer)
	hw_higrade=Column('hw_higrade',REAL)
	hw_lograde=Column('hw_lograde',REAL)
	hw_avgrade=Column('hw_avgrade',REAL)

class score(Base):
	__tablename__='score'
	score_id=Column('score_id',Integer,primary_key=True,unique=True,nullable=False)
	hw_id=Column('hw_id',String,ForeignKey('hw.hw_id'),nullable=False)
	stu_uid=Column('stu_uid',Integer,ForeignKey("stu.stu_uid"),nullable=False)
	stuid=Column('stuid',String,ForeignKey("stu.stuid"),nullable=False)
	score_solution=Column('score_solution',String)
	score_answer=Column('score_answer',String)
	score=Column('score',REAL,nullable=False)

class token(Base):
	__tablename__='token'
	token_id=Column('token_id',Integer,primary_key=True,unique=True,nullable=False)
	hw_id=Column('hw_id',String,ForeignKey("hw.hw_id"))
	stu_uid=Column('stu_uid',Integer,ForeignKey("stu.stu_uid"),nullable=False)
	stuid=Column('stuid',String,ForeignKey("stu.stuid"),nullable=False)
	token_type=Column('token_type',String,nullable=False)
	token=Column('token',String,nullable=False)
	token_expiration=Column('token_expiration',String,nullable=False)

class log(Base):
	__tablename__='log'
	log_id=Column('log_id',Integer,primary_key=True,unique=True,nullable=False)
	time=Column('time',String,nullable=False)
	log_type=Column('log_type',String)
	stu_uid=Column('stu_uid',Integer,ForeignKey("stu.stu_uid"))
	log=Column('log',String)