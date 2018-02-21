# rekit
A Python package for reproducible research.
## postman
Send and fetch email.
### createconfig(JSONname)
Create configuration file for postman.
### sendmail(configdict,to,subject,attachmentlist,_from,body)
Send email.
### retrievemail(configdict,inbox='INBOX')
Retrieve Mail from seleted inbox. Only unseen mail will be retrieved.
### getattach(msg,path,filename_withoutextension)
Get attachments from msg and save them into selected path with new name.

## models
Rekit SQLite models

## rekit_db
Act as a bridge between rekit and SQLite.
### create_db(basedir='./db',dbname='db.sqlite')
Initialize a SQLite database for rekit.
### eclassdict2db(eclassdict,db_url)
Write data in eclassdict into SQLite database.