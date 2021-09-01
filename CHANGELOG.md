2021-06-23
	ascii_reader:
		* Datatype from Data records is not dropped and now passed to result DataFrame
		* Error messages are now moved to separate module
		* Trim_res: Implemented correct handling of the value '00000', now not trimmed but passed as such
		* encode: Encoding is added. Default value is ANSI
	ascii_schema:
		* print_schema function added
	error_messages:
		* new module for all error message functions
	ascii_writer:
		* new module with the write_file function

2021-07-01
	ascii_writer:
		* Change the passing of the geocode format. If geo_frame and geo_dict with geocode and geolevel is given.
		  Then geostrucure is written correctly. Condition Geolevel = 90 or not.
		  If only geo_dict is given, then the geostructure of the data is taken
	error_messages:
		* Added error message to see if geolevel and geocode are passed in the geodict, to process correctly

2021-07-08
	ascii_write:
		* Count of data rows and count of geo structure rows is written if not overwritten in dict_header
		* Writer can write multi product files

2021-07-21
	ascii_reader:
		* An error message is printed if to_be_merged columns are empty. 
		* Zeros are inserted in case of empty values in a column with the datatype int. And 
          message is printed for these columns.