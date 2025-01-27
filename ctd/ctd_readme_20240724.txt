CTD readme

**************************************************************************************************************************************

The CTD used during the cruise was Sea-Bird Electronics underwater unit SBE9 plus and deck unit SBE11 plus.

The configuration file *.xmlcon file naming convention is defined by the cruise number, SBE9Plus serial number and file version letter.

The Pressure Offset value is directly from the factory calibration.
See deck test files for pressure offsets which can be calculated from deck test values subtracted from the factory calibrations so the pressure value on deck is ~0 db. 

If PAR sensor was included in the sensor setup, sensor was removed for casts over 2000m. The xmlcon file will still include the sensor.

**************************************************************************************************************************************

This folder contains the CTD data collected on the cruise. The data is sorted as follows:

\docs - documents, configuration info, text summaries of the CTD casts, etc.

   \docs\calibrations - sensor calibration documentation

   \docs\software_and_manuals - SBE data acquisition and processing software and manuals

   \docs\sbe_application_notes - SBE application notes which are pertinent to this CTD dataset

\proc - Processed ASCII CTD data. Data files and images of the CTD data after processing and derivations have been applied. A key to the headings of columns is included in \docs.

\procontrol - Files and routines used to process the raw CTD data used by the SBEDataProcessing-Win32 software.

\programfiles - Setup and plot display files used by the Seasave CTD data acquisition software.

\raw - Unprocessed CTD cast files.
 
Additional folders and files may exist for particular cruises.

**************************************************************************************************************************************

For meta data regarding instrument start & stop times and other events regarding this dataset, see the elog *.csv file in r2r\elog\

**************************************************************************************************************************************

***It is suggested that the scientists do their own processing of the CTD raw data for their specific purposes.***

The data have been preliminarily processed by the ship’s technician using Seabird recommended default parameters. These files should not be taken as the final processed product for analysis. Reference the Seasoft Data Processing manual in the \docs\software_and_manuals folder for more information.

**************************************************************************************************************************************

