import datetime
import sys
import shutil
import os
import subprocess

#-----------------------------
# input values from ENpro.BAT
#-----------------------------
#%1 - raw file 

raw_hex = sys.argv[1] + '.hex'
raw_xmlcon = sys.argv[1] + '.xmlCON'

BatchDir = 'C:\Windows'
PsaDir = 'C:\Users\bonny\Desktop\ctd\procontrol'
TxtFile = 'C:\Users\bonny\Desktop\ctd\procontrol\ENPRO.txt'
RawDir = 'C:\Users\bonny\Desktop\ctd\raw'
ProDir = 'C:\Users\bonny\Desktop\ctd\proc'
ArchiveDir = 'C:\Users\bonny\Desktop'

def check_file_paths(file_paths):
    """
    Check that all file paths are valid.
    
    Args:
        file_paths (list of str): List of file paths to check.
    
    Returns:
        bool: True if all file paths are valid, False otherwise.
    """
    all_valid = True
    
    for file_path in file_paths:
        # Check if the file exists
        if not os.path.isfile(file_path):
            print(f"File '{file_path}' does not exist or is not a file.")
            all_valid = False
        # Optionally check if the file is readable
        elif not os.access(file_path, os.R_OK):
            print(f"File '{file_path}' is not readable.")
            all_valid = False
    
    return all_valid

def main():
    


    file_paths = [
    BatchDir, PsaDir, TxtFile, RawDir, ProDir, ArchiveDir
    ]

    if check_file_paths(file_paths):
        print("All file paths are valid. Continuing with the script...")
        print('start CTD Processing of %1')
-------------------------------------------------------------------------
    #Copy .xmlcon file from raw to processed folder(s). -------------------------------------------------------------------
    shutil.copyfile(RawDir +  + '.xmlCON', archivedir + rawoutputfile + hexfileextension )
    print(f"'{raw_xmlcon}' copied to '{ProDir}'")
copy %RawDir%\%1.xmlCON %ProDir%
echo copy %RawDir%\%1.xmlCON  to %ProDir%
rem ------------------------------------------------------------------------- 
rem - Process Data.
rem -------------------------------------------------------------------------

%BatchDir%\sbebatch.exe %TxtFile% %RawDir% %1 %ProDir% %psaDir%

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
        shutil.copyfile(xmlfileinputpath, archivedir + xmlconoutputfile + xmlconfileextension )``

    else:
        print("One or more file paths are not valid. Exiting script.")

if __name__ == "__main__":
    main()



 