# File processor module for predefined files

This package comes with three functions to process predefined files.

Following, these three things will be explained:
1. How to get started
2. Three functions


## 1. How to get started

### Install and update from git

For an initial installation of the package.

```
pip install git+https://github.com/Simon-U/fixed-file-processor
```

For upgrading the package to the newest version.

```
pip install git+https://github.com/Simon-U/fixed-file-processor --upgrade
```

Please install pytest to run the test cases:
```
pip install pytest
```

### Import and use
The package can be installed with pip install command and the path to the right directory.

The following packages have to be imported to execute the test:
```
import os
import pkg_resources as pg
import file_processor as fp
from file_processor import read_file, write_file, print_schema
```

## 2. Functions

### file_reader.read_file()

The function can be then called as follows:
```
read_file(path)
```

The necessary parameter:
- path          : File path of the file

Optional parameters:
- to_be_merged  : Default = True. If True then one merged dataframe is returned
                  If False the results will be 4 dataframes
- study_type    : Default = None. By default, the study_type is read from the header line
- datatype      : Default = None. By default, the datatype is read from the header line
- lang          : Default = 'DE'. Currently, 'DE' and 'EN' are supported
- line_len      : Default = 140. Fixed line length of the file.
- encode        : Default='Latin-1'
A test dataset can be loaded:
```
path = os.sep.join([os.path.dirname(fp.__file__), 'Test_Data', 'kth1212.dat'])
df = read_file(path)
```

### file_schema.print_schema()

The function can be then called as follows:
```
print_schema("file_header","CSV")
```

It prints out the possible values to be passed to the dictionaries for the write function. 
Values are ('file_header', 'geo_structure', 'data_header', 'data_records'1)

The necessary parameter:

- _file_type          : Type of schema to be printed. Possible values are: 'header', 'geo', 'data header', 'data'
- _study_type         : Default is None. Then a list with possible values is returned
- _datatype           : Default is None. Then a list with possible values is returned 
  
Optional parameters:
- _version            : Default is None. Then the latest version is printed. Else a string can be passed
- _lang               : Default is 'DE'. 'EN' is also supported

### file_writer.write_file()

This function writes a dataframe to a predefined file in a predefined Schema. These can be printed with fp.print_schema()

```
write_file()
```

The only mandatory dictionary that has to be passed is the dict_header with studytype and datatype. The others are optional.
Not all schema parameters have to be passed, only the defined will be written in the file, the others will be left blank.
</br>The geostructure is special following options are possible:

1. Passing separate geo_frame and geo_dict (including Geocode [up to nine digits] and Geolevel [two digits]), whole geostruture will be written
2. Passing only geo_dict, geostrucutre of the data will be written. Format of the Geocode might be default left justified
   with tailing whitespaces if no Geolevel is passed. Correct format of Geocode can only be ensured with Geolevel.
3. Passing nothing, then nothing will be written.

The necessary parameter:

- folder : The path where the file should be stored **Including the name of the file but not the fil ending**
- frame : DataFrame which should be processed into .dat file
- dict_header: Dictionary for the header file. This dictionary is mandatory and the values for studytype and datatype have to be passed.
  The rest is optional. **Here only string values can be passed no array columns** 
  
Optional parameters:

- geo_frame : Default is None. If a dataframe is passed, then the geo structure from the passed dataframe is processed according to the dict_geo.
Therefore, the dict_geo has to be passed if a geo_frame is being passed.
- dict_geo : Dictionary that maps the geo data from the frame or geo_frame to the schema. Now geo structure will be added if neither a geo_frame, nor a 
dict_geo being passed.
- dict_data_header : Dictionary that maps the **string values** to the data_header_schema.
- dict_data : Dictionary that maps the data columns from the frame to the right columns from the schema.
- version : Version of the Schemas to be used. Default is the latest version.
- lang : Language to be used for the mapping. The default value is 'DE'
- encode        : Default='Latin-1'

Simple test using the test data:

```
# Import data from to df
path = os.sep.join([os.path.dirname(fp.__file__), 'Test_Data', 'kth1212.dat'])
df = fp.read_file(path)
df_head, df_geo, df_data_heder, df_data = fp.read_file(path, to_be_merged=False)
```
```
# Dictionaries for the writer function. Please add your path!
    dict_head = {
        'Berichtsart': "CSV",
        'Datei-Typ': 'KT',
        'Letzter Berichtsmonat  MM/JJJJ': '12/2012',
        'Waehrungseinheit': 'EUR',
        "Hierarchie-Kennung": "H",
        "Berichtszeitraum": "1212-1212",
        "Kundennummer": "99999",
        "Kundenname": "NEW Coorpo",
        "Preisdefinition": "HAP",
        "Anzahl Level": "3"
    }

    dict_geo = {
        "Geolevel": "Geolevel",
        "Geocode": "Geocode",
        "Geo Langname": "Geo Langname",
        "Geocode_hoehere_ebene": "Geocode_hoehere_ebene",
        "Geolevel_hoehere_ebene": "Geolevel_hoehere_ebene",
        "Levelbeschreibung": "Levelbeschreibung"
    }

    dict_data_header = {
        'Gruppencode': 'Gruppencode',
        "TC-Bezeichnung": "A01B0  PDF xxxxxx TEST ABC"
    }

    dict_data = {
        "Gruppencode": "Gruppencode",
        "Geolevel": "Geolevel",
        "Datentyp": "Datentyp",
        "Geocode": "Geocode",
        'Einheiten - fuer die Berichtsperiode': 'Einheiten - fuer die Berichtsperiode',
        'Umsatz (in Cent) - fuer die Berichtsperiode': 'Umsatz (in Cent) - fuer die Berichtsperiode',
    }

save_path = 
```
```
write_file(save_path, 'output', frame = df, dict_header=dict_head, geo_frame=df_geo, dict_geo = dict_geo,
            dict_data_header=dict_data_header, dict_data=dict_data)
```
## 3. Define structure files

The structure csv files are necessary to process the data correctly.
They can be accessed under file_processor/Schema. The first subdirectory is for the study_type,
following the version (e.g. v_3.7.0) and the language (DE or EN). There are currently eight files in each
language folder. Where in 3., 4. the ** are FM, SU and KT for the data_type. TC is being threatened with the KT structure.

1. one definition_header_record.csv
2. one definition_geostructure.csv
3. three definition_data_**.csv
4. three definition_record**.csv


The structure files are derived from the definition tables in the description files as follows:

The files are processed with the same steps for the different languages.<br/>
The header of the columns is not important, but **the order must be always the same!!!**<br/>
**The files need to be saved as csv and semicolon ";" delimited!!**
The description will be the column names in the output.


    1. Layout of the Header Record 
        1.1 Copy first 4 columns (Position, Length, Description, Type) to Excel
        1.2 Change "Alphanumeric" to False and "Numeric" to True
            !!! Exception is "Latest Month of Report  MM/YYYY" which needs to be False !!!
        1.3 Add column "Needed". Define with True which columns should be processed and not with False
        1.4 Add column "to_be_added". Defining which columns should be added to the merged output
            Currently "Latest Month of Report  MM/YYYY" and "Report Period"
        1.5 Add column "leading_tailing" with the following values.
            0: Default
            1: Right justified with leading zeros
            2: Right justified with leading whitespaces
            3: Left justified with tailing whitespaces
            4: Right justified with leading zeros !! and sign (+/-). Relevant for data columns !!
        1.6 Save in the correct subdirectory depending on study_type, version and language
        1.7 The name always needs to be "definition_header_record", and the file need to be stored as csv and
            delimited with ;
    
    2. Definition Record Geo Structure  
        2.1 Copy first 4 columns (Position, Length, Description, Type) to Excel
        2.2 Change "Alphanumeric" to False and "Numeric" to True
        2.3 Add column "Needed". Define with True which columns should be processed and not with False
        2.4 Add column "to_be_dropped". Defining which columns will be dropped before merging all tables
            Currently "Record Type" and "Data Type"
        2.5 Add column "to_be_merged_on". Defining which columns will be used to merge the geostructore to the data table
            Currently "Geolevel" and "Geocode"
        2.5 Add column "leading_tailing" with the following values.
            0: Default
            1: Right justified with leading zeros
            2: Right justified with leading whitespaces
            3: Left justified with tailing whitespaces
            4: Right justified with leading zeros !! and sign (+/-). Relevant for data columns !!
        2.7 Save in the correct subdirectory depending on study_type, version and language
        2.8 The name always needs to be "definition_geostructure", and the file need to be stored as csv and
            delimited with ;
    
    3. Definition of record for all datatype 
        3.1 Copy first 4 columns (Position, Length, Description, Type) to Excel
        3.2 Change "Alphanumeric" to False and "Numeric" to True
        3.3 Add column "Needed". Define with True which columns should be processed and not with False
        3.4 Add column "to_be_dropped". Defining which columns will be dropped before merging all tables
            Currently "Record Type" and "Data Type"
        3.5 Add column "to_be_merged_on". Defining which columns will be used to merge the record file to the  data table
            Currently "ATC Code", "Product Code" and "Pack Code"
        3.6 Add column "leading_tailing" with the following values.
            0: Default
            1: Right justified with leading zeros
            2: Right justified with leading whitespaces
            3: Left justified with tailing whitespaces
            4: Right justified with leading zeros !! and sign (+/-). Relevant for data columns !!
        3.7 Save in the correct subdirectory depending on study_type, version and language
        3.8 The name always needs to be "definition_record_**" where ** is FM, SU or KT.
            In case of TC the KT will be picked. The file need to be stored as csv and delimited with ;
    
    4. Definition of data for all datatype 
        4.1 Copy first 4 columns (Position, Length, Description, Type) to Excel
        4.2 Change "Alphanumeric" to False and "Numeric" to True
        4.3 Add column "Needed". Define with True which columns should be processed and not with False
        4.4 Add column "to_be_dropped". Defining which columns will be dropped before merging all tables
            Currently "Record Type", "Data Type", "Sign for Units", "Sign for Values" and "Sign for Counting Units"
        4.5 Add column "leading_tailing" with the following values.
            0: Default
            1: Right justified with leading zeros
            2: Right justified with leading whitespaces
            3: Left justified with tailing whitespaces
            4: Right justified with leading zeros !! and sign (+/-). Relevant for data columns !!
        4.6 Save in the correct subdirectory depending on study_type, version and language
        4.7 The name always needs to be "definition_data_**" where ** is FM, SU or KT.
            In case of TC the KT will be picked. The file need to be stored as csv and delimited with ;
