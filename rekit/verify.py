import binascii, os
def mailchecker(msg,criteriondict): #Maybe define it elsewhere
	subjectlist=convert.extract_data_from_curly_brackets(msg['subject'])

def generate_token(par):
	strToken=binascii.b2a_base64(os.urandom(6))[:-1]
	print(strToken)
	return strToken
