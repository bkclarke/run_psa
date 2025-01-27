import datetime
import sys
import shutil

#-----------------------------
# input values from ENpro.BAT
#-----------------------------
#%1 - raw file 
#%2 - cast specific xmlcon file 
#%3 - archive directory
#%4 - raw directory 


#set current date and time object to current_date
current_date = datetime.datetime.now().strftime('%Y%m%d_%H%M')

#------------------------------
# assign %1-%4 input to objects 
#------------------------------
rawfile=sys.argv[1]
rawfile_edit=rawfile[:-4] #Remove .hex from tail end of filename, to be concatenated with datetime
xmlconfile=sys.argv[2]
xmlconfile_edit=xmlconfile[:-7] #Remove .hex from tail end of filename, to be concatenated with datetime
archivedir=sys.argv[3]
rawdir=sys.argv[4]

#join rawfiles without .hex tail with current date
rawoutputfile = ''.join([rawfile_edit,'_',current_date])
xmlconoutputfile = ''.join([xmlconfile_edit,'_',current_date])

#path of input files to copy
rawfileinputpath = rawdir + rawfile
xmlfileinputpath = rawdir + xmlconfile

hexfileextension = '.hex'
xmlconfileextension = '.xmlcon'

#copy raw input file to archive directory with date appended to filename
shutil.copyfile(rawfileinputpath, archivedir + rawoutputfile + hexfileextension )
shutil.copyfile(xmlfileinputpath, archivedir + xmlconoutputfile + xmlconfileextension )