from pyorgtex import convert
from . import rekit_db, models
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *

def verify(subjectlist,db_url):
	if(subjectlist[1]=='Request'):
		engine=create_engine(db_url)
		Session=sessionmaker(bind=engine)
		session=Session()
		queryresult=session.query(models.token).filter(models.token.stuid==subjectlist[3],models.token.token_type=='ACCESS',models.token.token_expiration=='PERMANENT').all()
		if(len(queryresult)==1):
			if(queryresult[0].token==subjectlist[4]):
				if(subjectlist[2]=='Manual'):
					return True
				elif(subjectlist[2]=='Score'):
					return True
				elif(subjectlist[2][0:2]=='HW'):
					strid=subjectlist[2][2:]
					if(strid==''):
						return False
					else:
						hw_id=int(strid)
						queryresult=session.query(models.hw).filter(models.hw.hw_id==hw_id).all()
						if(len(queryresult)==1):
							return queryresult[0].hw_available
						else:
							return False
				else:
					return False
			else:
				return False
		else:
			return False
	if(subjectlist[1]=='Submit'):
		Session=sessionmaker(bind=engine)
		session=Session()
		queryresult=session.query(models.token).filter(models.token.stuid==subjectlist[3],models.token.token_type=='HW').all()

def requesthandler(msg,str_msgsubject,db_url,PATHdict={}):
	subjectlist=convet.extract_data_from_curly_brackets(str_msgsubject)
