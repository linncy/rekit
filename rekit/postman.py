import smtplib
from threading import Thread
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pyorgtex.convert import *
def createconfig(JSONname):
	newdict={}
	newdict['MAIL_ADDRESS']='example@gmail.com'
	newdict['MAIL_SERVER']='smtp.googlemail.com'
	newdict['MAIL_PORT']=587
	newdict['MAIL_USE_TLS']=True
	newdict['MAIL_USE_SSL']=False
	newdict['MAIL_USERNAME']='mailusername'
	newdict['MAIL_PASSWORD']='mailpassword'
	dict2json(newdict,mail_conf.json)
	print(JSONname +'created.')
	
def sendmail(configdict,to,subject,attachmentlist,_from='Reproducible Hw',body='This is an email sent from juno.\n Juno lives at the 13th floor, ICE \n Good Luck! '):
	msg = MIMEMultipart()
	msg['Subject']=subject
	msg['To']=to
	msg['From']=_from
	msg.preamble=body
	for item in attachmentlist:
		attachment=MIMEText(open(item,'rb').read(),'base64','utf-8')
		attachment["Content-Type"]='application/octet-stream'
		attachment["Content-Disposition"]='attachment; filename="'+extractFilename(item)+'"'
		msg.attach(attachment)
	server = smtplib.SMTP(configdict['MAIL_SERVER'],configdict['MAIL_PORT'])
	server.set_debuglevel(1)
	server.login(newdict['MAIL_ADDRESS'],['MAIL_PASSWORD'])
	server.sendmail(msg)
	server.quit()
