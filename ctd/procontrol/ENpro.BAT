@ECHO OFF
rem -------------------------------------------------------------------------
rem -
rem - !!! Before processing, SBEDataProcessing_Win32_V7_18c.exe or more recent version, must be installed in C:\Program Files\Sea-Bird\SBEDataProcessing-Win32 and
rem - !!! SBEBatch.exe must be copied manually from C:\Program Files\Sea-Bird\SBEDataProcessing-Win32 to C:\WINDOWS
rem -
rem - Process CTD data with SBE Windows processing.
rem -
rem - This batch file is a shell which runs SBEbatch.exe  Define the input text/batch file as 
rem - well as directories for input, output and .psa files.
rem -
rem - Assumptions:
rem -	1) The .CON file is in the raw data directory with the .HEX file
rem -	2) The processed data directory is different than the raw data directory
rem -	3) The .psa file will have the same name as the processing file it sets up
rem -		Example: AlignCtd will use AlignCtd.psa as a set up file
rem -		Exception: There might be two .psa files for DERIVE
rem -			   they are derive.psa and deriveO2.psa 
rem -
rem - Command line argument (%1) is the raw data file name without extention
rem -	Example: If raw CTD data file is CTD001.hex you would enter "CTD001" 	
rem -
rem -
rem -------------------------------------------------------------------------
rem -------------------------------------------------------------------------
rem - Define batch/text file and directories with the "SET" statement
rem 	Note: Do not include final backslash for directories
rem
rem		BatchDir - Location of SBEbatch.exe
rem 	psaDir  - Program Set Up directory (.psa)
rem		TxtFile - Path and name of SBE "batch file" containing processing instructions 	
rem 	RawDir  - Raw data directory (input)
rem 	ProDir - Processed directory (output)
rem
rem -------------------------------------------------------------------------
set BatchDir=C:\Windows
set psaDir=C:\Users\bonny\Desktop\ctd\procontrol
set TxtFile=C:\Users\bonny\Desktop\ctd\procontrol\ENPRO.txt
set RawDir=C:\Users\bonny\Desktop\ctd\raw
set ProDir=C:\Users\bonny\Desktop\ctd\proc
set ArchiveDir=C:\Users\bonny\Desktop\

rem -------------------------------------------------------------------------
rem - Be sure castname was entered, be sure files and directories exist
rem -------------------------------------------------------------------------
if "%1"=="" goto NOARG
echo %1
if not exist %psaDir%\EN_Datcnv.psa goto BADENV
if not exist %TxtFile% goto BADENV
if not exist %RawDir%\%1.HEX goto BADENV
if not exist %BatchDir%\SBEbatch.exe goto BADENV

rem -------------------------------------------------------------------------
rem - Say what's happening.
rem -------------------------------------------------------------------------
echo.
echo CTD Processing of %1
echo Batch Dir : %BatchDir%
echo Batch File: %TxtFile%
echo Input from: %RawDir%
echo Output to : %ProDir%
echo psa files : %psaDir%

rem -------------------------------------------------------------------------
rem - Copy .xmlcon file from raw to processed folder(s). 
rem - Process Data. 
rem -------------------------------------------------------------------------
copy %RawDir%\%1.xmlCON %ProDir%
echo copy %RawDir%\%1.xmlCON  to %ProDir%
rem ------------------------------------------------------------------------- 
rem - Process Data. 
rem -------------------------------------------------------------------------

%BatchDir%\sbebatch.exe %TxtFile% %RawDir% %1 %ProDir% %psaDir%

rem ------------------------------------------------------------------------- 
rem - Copy files to data archive. 
rem -------------------------------------------------------------------------
echo Archiving .hex and .xmlcon files to %ArchiveDir% 
python C:\Users\bonny\Desktop\ctd\procontrol\ctd_archive.py \%1.hex \%1.xmlCON %ArchiveDir% %RawDir%

rem ------------------------------------------------------------------------
rem - Done: say bye, go home
rem ------------------------------------------------------------------------
echo. 
echo Batch processing of %1 launched...

goto END

@ECHO OFF

rem -------------------------------------------------------------------------
rem - Error handlers here.
rem -------------------------------------------------------------------------

:NOARG
echo.
echo.
echo Usage: %0 castname
echo.
echo castname is the name of the raw data file without path
echo or .HEX extention
echo.
echo	Example: If the raw CTD data is "C:\CtdData\CTD001.hex" you
echo		 would enter "CTD001"
echo.
goto END

:BADENV
echo.
echo Invalid setup parameter(s) in %0 as follows:
if not exist %TxtFile%    echo Batch File does not exist: %TxtFile%
if not exist %RawDir%\%1.hex    echo Raw CTD data file does not exist: %RawDir%\%1.hex
if not exist %BatchDir%\SBEbatch.exe echo Batch processing file not found: %BatchDir%\SBEbatch.exe
if not exist %psaDir%\EN_Datcnv.psa echo Batch PSA file not found: %psaDir%\EN_Datcnv.psa
echo.

goto END

rem -------------------------------------------------------------------------
rem - Clean up
rem -------------------------------------------------------------------------

:END
set BatchDir=
set psaDir=
set TxtFile=                         
set RawDir=
set ProDir=
