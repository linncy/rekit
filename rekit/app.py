from . import models, rekit_db, postman
from pyorgtex import convert, generate, orgexport
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

def generate_manual_single(stuid,db_url,manualORGname,dirname='./',exportformat='pdf',dependencylist=[]):
	newdict={'course':'','term':'','classnumber':'','stuid':'','stu_name':'','token':'','token_type':'ACCESS','token_expiration':'','message':''}
	engine = create_engine(db_url)
	Session=sessionmaker(bind=engine)
	session=Session()
	querydict=['course','term','classnumber']
	for keyword in querydict:
		queryresult=session.query(models.info).filter(models.info.info_name==keyword).one()
		newdict[keyword]=queryresult.info_value
	queryresult=session.query(models.stu).filter(models.stu.stuid==stuid).all()
	if(len(queryresult)==1):
		newdict['stuid']=stuid
		newdict['stu_name']=queryresult[0].stu_name
		queryresult=session.query(models.token).filter(models.token.stuid==stuid,models.token.token_type=='ACCESS').all()
		newdict['token']=queryresult[0].token
		newdict['token_type']='ACCESS'
		newdict['token_expiration']=newdict['term']
	else:
		newdict['stuid']='Invalid Student ID'
		newdict['stu_name']='N/A'
		newdict['token']='N/A'
		newdict['token_type']='N/A'
		newdict['token_expiration']='N/A'
		newdict['message']=stuid+' is an invalid student ID number. There is no match (or multiple matches) in database. Please check the student\'s course registration status.'
	generate.generate_from_par(newdict,manualORGname,exportformat,dirname,dependencylist)

def generate_manual_all(db_url,manualORGname,dirname,exportformat='pdf',dependencylist=[]):
	engine = create_engine(db_url)
	Session=sessionmaker(bind=engine)
	session=Session()
	queryresult=session.query(models.stu).all()
	for item in queryresult:
		generate_manual_single(item.stuid,db_url,manualORGname,dirname,exportformat,dependencylist)

def requesthandler(configdict,INBOXname,PATHdict={}):
	