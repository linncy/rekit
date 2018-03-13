from subprocess import call
import convert, orgexport
import sys,os
def generate_from_classjson(JSONname,ORGname,exportformat='pdf',dirname='./',dependencylist=[]):
	if not os.path.isfile(JSONname):
		print("generate_from_classjson Error: " + JSONname + " doesn't exist")
		sys.exit()
	classdict=convert.json2dict(JSONname)
	for i in range(classdict['numofstu']):
		generate_from_par(classdict['student'][str(i)],ORGname,exportformat,dirname,dependencylist)

def generate_from_par(dictPar,ORGname,exportformat='pdf',dirname='./',dependencylist=[]):
	if not os.path.isfile(ORGname):
		print("generate_from_par Error: " + ORGname + " doesn't exist")
		sys.exit()
	if os.path.exists('./pyorgtex_tmp/'):
		call(['rm','-rf','./pyorgtex_tmp'])
	call(['mkdir','pyorgtex_tmp'])
	print('tmp directory created')
	if(len(dependencylist)!=0):
		for i in range(len(dependencylist)):
			call(['cp','-r',dependencylist[i],'./pyorgtex_tmp/'+convert.extractFilename(dependencylist[i])])
			print(dependencylist[i]+ 'copied')
	if not os.path.exists(dirname):
		newdir=dirname[2:-1]
		print('Create the directory: ' + newdir)
		call(['mkdir',newdir])
	call(['cp','-r',ORGname,'./pyorgtex_tmp/'+dictPar['stuid']+'.org'])
	convert.dict2json(dictPar,'./pyorgtex_tmp/'+dictPar['stuid']+'.json')
	if(exportformat=='pdf'):
		orgexport.export2pdf('./pyorgtex_tmp/'+dictPar['stuid']+'.org')
	call(['cp','-r','./pyorgtex_tmp/'+dictPar['stuid']+'.pdf',dirname+dictPar['stuid']+'.pdf'])
	print(dictPar['stuid']+' Done!')
