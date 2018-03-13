from pyorgtex import convert
from . import rekit_db, models, postman, app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *

def verify(subjectlist,db_url):
	if(len(subjectlist)!=5):
		return [False,'Illegal mail subject.']
	if(subjectlist[1]=='Request'):
		engine=create_engine(db_url)
		Session=sessionmaker(bind=engine)
		session=Session()
		queryresult=session.query(models.token).filter(models.token.stuid==subjectlist[3],models.token.token_type=='ACCESS',models.token.token_expiration=='PERMANENT').all()
		if(len(queryresult)==1):
			if(queryresult[0].token==subjectlist[4]):
				if(subjectlist[2]=='Manual'):
					return [True]
				elif(subjectlist[2]=='Score'):
					return [True]
				elif(subjectlist[2][0:2]=='HW'):
					strid=subjectlist[2][2:]
					if(strid==''):
						return [False,'Illegal Homework ID.']
					else:
						hw_id=int(strid)
						queryresult=session.query(models.hw).filter(models.hw.hw_id==hw_id).all()
						if(len(queryresult)==1):
							return queryresult[0].hw_available
						else:
							return [False,'Unavailable Homework.']
				else:
					return [False,'Illegal request']
			else:
				return [False,'Wrong student ID or ACCESS token']
		else:
			return [False,'Wrong Student ID or ACCESS token']
	if(subjectlist[1]=='Submit'):
		Session=sessionmaker(bind=engine)
		session=Session()
		queryresult=session.query(models.token).filter(models.token.stuid==subjectlist[3],models.token.token_type=='HW').all()

def requesthandler(configdict,msg,str_msgsubject,db_url,PATHdict={}):
	subjectlist=convert.extract_data_from_curly_brackets(str_msgsubject)
	verifyresult=verify(subjectlist,db_url)
	try:
		stuid=subjectlist[3]
	except:
		stuid=''
	if(not(verifyresult[0])):
		postman.sendmail(configdict,msg['Return-Path'][1:-1],'Bad Request',[],'Juno',body='Bad Request\nThis error may be caused by:\n'+verifyresult[1]+'\n')
		newlog=models.log(time=app.gettime(),log_type='Request',stuid=stuid,log='Error: '+verifyresult[1]+' ',+' From: '+msg['From'],+' Date: ')
def submithandler(configdict,msg,str_msgsubject,db_url,PATHdict={}):
	return 0