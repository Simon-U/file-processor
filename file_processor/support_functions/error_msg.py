import pathlib
import os


def get_immediate_subdirectories(dir_path):
    """
    The function returns the immediate subdirectories of the passed path

    Args:
        dir_path (string) : The directory under which to look for subdirectories

    Returns:
        out (List) : Returns list of the subdirectories

    """

    # Goes through the subdirectory of a_dir and returns the result
    return [f.name for f in os.scandir(dir_path) if f.is_dir()]


def error_msg_study_type(_study_type):
    """
    Error message for study type

    Args:
        _study_type (String): Expected string value for the study type

    Returns:
        Returns error message depending on the value on study type
    """

    # raise error if study type is empty
    if _study_type is None:
        raise ValueError('No study type found. Please pass the correct study type')

    path = pathlib.Path(__file__).parent.parent / 'Schema'
    directory_list = get_immediate_subdirectories(path)

    # raise error if study type is not found in the Schema dir
    if _study_type not in directory_list:
        raise ValueError('The study type %s could not be found in %s' % (_study_type, directory_list))


def error_msg_version(_version, _study_type):
    """
    Error message for study type

    Args:
        _version (String)   : Expected string value for the version
        _study_type (String): Expected string value for the study type

    Returns:
        Returns error message depending on the value of version
    """

    path = pathlib.Path(__file__).parent.parent / 'Schema' / _study_type
    directory_list = get_immediate_subdirectories(path)

    # raise error if version is not found in the directory of the study
    if _version not in directory_list:
        raise ValueError('Incorrect version %s. Default None where the latest will be picked.'
                         'Or select one of the following %s' % (_version, directory_list))


def error_msg_lang(_lang, _version, _study_type):
    """
    Error message for language

    Args:
        _lang (String) : Expected value is a string of length 2 for the language e.g. 'DE'
        _version (String)    : Expected string value for the version
        _study_type (String): Expected string value for the study type

    Returns:
        Returns error message depending on the language
    """

    values = ['DE', 'EN']
    # Checks if the value for language is right
    if _lang not in values:
        raise ValueError('Incorrect language %s. Default DE. Or select one of the following %s' % (_lang, values))

    # checks if the language is also in the directory
    path = pathlib.Path(__file__).parent.parent / 'Schema' / _study_type / _version
    directory_list = get_immediate_subdirectories(path)

    if _lang not in directory_list:
        raise ValueError('Language %s not found for the %s in the study %s. Following languages are found %s'
                         % (_lang, _version, _study_type, directory_list))


def error_msg_datatype(_datatype, _lang, _version, _study_type):
    """
    Error message for language

    Args:
        _datatype (String): Expected value is a string for the datatype e.g. 'FM' or 'SU'
        _lang (String) : Expected value is a string of length 2 for the language e.g. 'DE'
        _version (String)    : Expected string value for the version
        _study_type (String): Expected string value for the study type

    Returns:
        Returns error message depending on the language
    """

    values = ['FM', 'SU', 'TC', 'KT']

    # Checks if the value for datatype found in the header is one of the known
    if _datatype not in values:
        raise ValueError('Unknown value for datatype found: %s. Please select one of the following %s' %
                         (_datatype, values))

    # checks if the needed files for the datatype are in the directory
    path = pathlib.Path(__file__).parent.parent / 'Schema' / _study_type / _version / _lang
    directory_list = [f for f in os.listdir(path) if f.endswith('.csv')]

    if ('definition_data_' + _datatype + '.csv') not in directory_list:
        raise ValueError('definition_data_%s not found. Following are found %s' % (_datatype, directory_list))
    
    if ('definition_record_' + _datatype + '.csv') not in directory_list:
        raise ValueError('definition_record_%s not found. Following are found %s' % (_datatype, directory_list))


def error_msg_file_type(_file_type):
    """
    Error message for file type

    Args:
        _file_type (String): Expected string value for the file type

    Returns:
        Returns error message depending on the value on study type
    """

    values = ['file_header', 'geo_structure', 'data_header', 'data_records']

    # raise error for file type
    if _file_type not in values:
        raise ValueError('Unknown value for file type found: %s. Please select one of the following %s'
                         % (_file_type, values))


def error_msg_geolevel(_dict_geo):
    """

    Args:
        _dict_geo: Dict of the geo structure to see if the geolevel is passed

    Returns:
        Returns error message if there is no geo level and geo code
    """
    if 'Geocode' not in _dict_geo:
        raise ValueError('Geocode is not found in the geo_dict. Please pass a column')
    if 'Geolevel' not in _dict_geo:
        raise ValueError('Geolevel is not found in the geo_dict. Please pass a column')


def error_msg_merged_columns(_dataframe_to_check, _type, _to_be_merged):
    """

    Args:
        _dataframe_to_check: the dataframe which will be checked for the to_be_merged columns
        _type: either data_records, data_header or geo_structure, provided for the message
        _to_be_merged: the to be merged columns as list

    Returns:
        Returns a error message
    """
    for column in _to_be_merged:
        if (_dataframe_to_check[column] == '').all():
            raise ValueError('The column %s is needed for the merge but empty in the %s. '
                             'Please provide the %s in the file or pass to_be_merged as False'
                             % (column, _type, column))
