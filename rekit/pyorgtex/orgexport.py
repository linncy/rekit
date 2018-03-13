from subprocess import call
import sys,os
#----Define some environmental variables here------#
EMACS_INIT_PATH='/Users/Lin/.emacs.d/init.el'
#--------------------------------------------------#
def export2pdf(ORGname):
	if not os.path.isfile(ORGname):
        	print("export2pdf Error: " + ORGname + " doesn't exist")
    		sys.exit()
	call(['emacs',ORGname,'--batch','-l',EMACS_INIT_PATH,'-f','org-babel-execute-buffer','-f','org-latex-export-to-pdf','--kill'])

def export2tex(ORGname):
	if not os.path.isfile(ORGname):
        	print("export2pdf Error: " + ORGname + " doesn't exist")
    		sys.exit()
	call(['emacs',ORGname,'--batch','-l',EMACS_INIT_PATH,'-f','org-babel-execute-buffer','-f','org-latex-export-to-latex','--kill'])

def export2html(ORGname):
	if not os.path.isfile(ORGname):
        	print("export2pdf Error: " + ORGname + " doesn't exist")
    		sys.exit()
	call(['emacs',ORGname,'--batch','-l',EMACS_INIT_PATH,'-f','org-babel-execute-buffer','-f','org-html-export-to-html','--kill'])

def export2ascii(ORGname):
	if not os.path.isfile(ORGname):
        	print("export2pdf Error: " + ORGname + " doesn't exist")
    		sys.exit()
	call(['emacs',ORGname,'--batch','-l',EMACS_INIT_PATH,'-f','org-babel-execute-buffer','-f','org-ascii-export-to-ascii','--kill'])

