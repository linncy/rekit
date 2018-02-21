from sqlalchemy import Column, Integer, String, REAL, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
import binascii, os
Base = declarative_base()

class info(Base):
	__tablename__='info'
	info_id=Column('info_id',Integer,primary_key=True,unique=True,nullable=False)
	info_name=Column('info_name',String)
	info_value=Column('info_value',String)

class stu(Base):
	__tablename__='stu'
	stu_uid=Column('info_id',Integer,primary_key=True,unique=True,nullable=False)
	stuid=Column('stuid',String,nullable=False,unique=True)
	stu_name=Column('stu_name',String)
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
	score=Column('score',REAL,nullable=False)

class token(Base):
	__tablename__='token'
	token_id=Column('token_id',Integer,primary_key=True,unique=True,nullable=False)
	hw_id=Column('hw_id',String,ForeignKey("hw.hw_id"),nullable=False)
	stu_uid=Column('stu_uid',Integer,ForeignKey("stu.stu_uid"),nullable=False)
	stuid=Column('stuid',String,ForeignKey("stu.stuid"),nullable=False)
	token=Column('token',String,nullable=False)

	def generate_token(self):
		strToken=binascii.b2a_base64(os.urandom(6))[:-1]
		return strToken

class log(Base):
	__tablename__='log'
	log_id=Column('log_id',Integer,primary_key=True,unique=True,nullable=False)
	time=Column('time',String,nullable=False)
	stu_uid=Column('stu_uid',Integer,ForeignKey("stu.stu_uid"),nullable=False)
	log=Column('log',String)