import smtplib, imaplib, email
from threading import Thread
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pyorgtex.convert import *
def createconfig(JSONname):
	newdict={}
	newdict['MAIL_ADDRESS']='example@gmail.com'
	newdict['MAIL_SMTP_SERVER']='smtp.gmail.com'
	newdict['MAIL_IMAP_SERVER']='imap.gmail.com'
	newdict['MAIL_SMTP_PORT']=587
	newdict['MAIL_IMAP_PORT']=993
	newdict['MAIL_USE_TLS']=True
	newdict['MAIL_USE_SSL']=True
	newdict['MAIL_USERNAME']='mailusername'
	newdict['MAIL_PASSWORD']='mailpassword'
	dict2json(newdict,JSONname)
	print(JSONname +'created.')

def sendmail(configdict,to,subject,attachmentlist,_from='Juno',body='This is an email from Juno.\nJuno lives at 13th floor, ICE \nGood Luck! '):
	msg = MIMEMultipart()
	msg['Subject']=subject
	msg['To']=to
	msg['From']=_from
	msg.preamble=body
	msg.attach(MIMEText(body))
	for item in attachmentlist:
		attachment=MIMEText(open(item,'rb').read(),'base64','utf-8')
		attachment["Content-Type"]='application/octet-stream'
		attachment["Content-Disposition"]='attachment; filename="'+extractFilename(item)+'"'
		msg.attach(attachment)
	server = smtplib.SMTP(configdict['MAIL_SMTP_SERVER'],configdict['MAIL_SMTP_PORT'])
	server.set_debuglevel(1)
	server.ehlo()
	if(configdict['MAIL_USE_SSL']==True):
		server.starttls()
	server.login(configdict['MAIL_ADDRESS'],configdict['MAIL_PASSWORD'])
	server.sendmail(_from,to,msg.as_string())
	server.quit()

def retrievemail(configdict,inbox='INBOX'):
	if configdict['MAIL_USE_SSL']==True:
		imapserver=imaplib.IMAP4_SSL(port=configdict['MAIL_IMAP_PORT'],host=configdict['MAIL_IMAP_SERVER'])
	else:
		imapserver=imaplib.IMAP4(port=configdict['MAIL_IMAP_PORT'],host=configdict['MAIL_IMAP_SERVER'])
	imapserver.login(configdict['MAIL_ADDRESS'],configdict['MAIL_PASSWORD'])
	imapserver.select(inbox)
	typ, data = imapserver.search(None, 'unseen') #Fetch unread mail only
	msglist=[]
	for num in data[0].split():
		typ, data = imapserver.fetch(num, '(RFC822)')
		imapserver.store(num,'+FLAGS','\\Seen') #Marked mail as seen
		msg = email.message_from_string(data[0][1].decode('utf-8')) 
		msglist.append(msg)
	imapserver.close()
	imapserver.logout()
	return msglist

def getattach(msg,path,filename_withoutextension):
	for part in msg.walk():
		if part.get_content_maintype() == 'multipart':
			continue
		if part.get('Content-Disposition') is None:
			continue
		attachmentname = part.get_filename()
		attchmentnamelist=splitFilename(attachmentname)
		data = part.get_payload(decode=True)
		if not data:
			continue
		marker=2
		fname=path+filename_withoutextension+'.'+attchmentnamelist[-1]
		while(os.path.isfile(fname)):
			fname=path+filename_withoutextension+'_'+str(marker)+'.'+attchmentnamelist[-1]
			marker+=1
		f  = open(fname, 'w')
		f.write(str(data))
		f.close()

def mailchecker(msg,criteriondict): #Maybe define it elsewhere
	subjectlist=convert.extract_data_from_curly_brackets(msg['subject'])