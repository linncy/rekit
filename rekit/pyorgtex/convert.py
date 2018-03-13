#coding=utf-8
import sys,os,re,csv,json,xlrd

def csv2dict(CSVname):
	if not os.path.isfile(CSVname):
		print("csv2list Error: " + CSVname + " doesn't exist")
		sys.exit()
	newdict={}
	with open(CSVname, "r") as csvfile:
		csvreader = csv.reader(csvfile, delimiter=';', quotechar='\n')
		#print csvreader.next()
		for eachrow in csvreader:
			newdict[eachrow[0]]=eachrow[1]
	return newdict

def fdf2csv(FDFname):
	if not os.path.isfile(FDFname):
		print("fdf2csv Error: " + FDFname + " doesn't exist")
		sys.exit()
	FDF_file = open(FDFname, "r")
	FDF = FDF_file.read()
	FDF_list = re.sub("(þÿ|FEFF)", "", FDF)
	pattern = re.compile('\/T\(([^)]*)\)\/V[(/<]([^>)]*)')
	FDF_list = re.findall(pattern, FDF_list)
	csv_key = []
	csv_value = []
	#csv_head=['Key','Value']
	for i in FDF_list:
		csv_key.append(i[0])
		csv_value.append(i[1])
	csv_file = re.sub("\.fdf", ".csv", FDFname)
	with open(csv_file, "w") as csvfile:
		wr = csv.writer(csvfile, delimiter=";", lineterminator='\n')
		#wr.writerow(csv_head)
		for i in range(len(csv_key)):
			aRow=[csv_key[i],csv_value[i]]
			wr.writerow(aRow)
	csvfile.close()
	return csv_file

def json2dict(JSONname):
	if not os.path.isfile(JSONname):
		print ("json2dict Error: " + JSONname + " doesn't exist")
		sys.exit()
	JSON_file=open(JSONname, "r")
	jsondict=json.loads(JSON_file.read())
	JSON_file.close()
	return jsondict

def dict2json(jsondict,JSONname):
	with open(JSONname, 'w') as jsonfile:
		json.dump(jsondict, jsonfile)
	jsonfile.close()
	return JSONname

def extractFilename(path):
	if(path==''):
		return('illegalpath')
	newlist=re.split('/',path)
	if(path[-1]=='/'):
		return newlist[-2]
	else:
		return newlist[-1]

def splitFilename(filename):
	if('.' in filename):
		newlist=re.split('\.',filename)
		return newlist
	else:
		return []

def eclass2dict(eclassXLSname):
	if not os.path.isfile(eclassXLSname):
		print("eclass2dict Error: " + eclassXLSname + " doesn't exist")
		sys.exit()
	newdict={}
	eclassXLSdata = xlrd.open_workbook(eclassXLSname)
	table = eclassXLSdata.sheet_by_index(0) 
	newdict['term']=table.row_values(0)[0]
	newdict['course']=table.row_values(0)[1].replace(' ','')
	newdict['classnumber']=table.row_values(2)[1]
	newdict['numofstu']=table.nrows-2
	newdict['student']={}
	for i in range(newdict['numofstu']):
		newsubdict={}
		newsubdict['stuid']=table.row_values(i+2)[2]
		newsubdict['name']=table.row_values(i+2)[4]
		newsubdict['numofhw']=0
		newsubdict['finalhwgrade']=-1
		newsubdict['hw']={}
		newdict['student'][str(i)]=newsubdict
	return newdict

def extract_data_from_curly_brackets(string):
	pattern = re.compile(r'(?<=\{)[^}]*(?=\})')  
	result = pattern.findall(string)
	return result