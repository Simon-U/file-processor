import pandas as pd
from pathlib import Path

from .error_msg import get_immediate_subdirectories, error_msg_study_type, error_msg_version,\
    error_msg_lang, error_msg_datatype, error_msg_file_type


def print_schema(file_type=None, study_type=None, datatype=None, version=None, lang='DE'):
    """
    Function that prints the schema
    Args:
        file_type: String value 'file_header' for header line
                                 'geo_structure' for geo structure
                                 'data_header' for data header
                                 'data_records' for data structure
        study_type: String value for study type e.g. 'RPM'
        datatype:  String value for data type e.g. 'SU'
        version: String value for version. By default latest is taken
        lang:  String value for language. Default is 'DE'

    Returns:
        Prints the Schema out
    """

    # Error message for file type
    error_msg_file_type(file_type)

    # Check study type. And if not found then give error message
    error_msg_study_type(study_type)

    # check version. And if None, get the highest version
    # If the version is passed manually then it will be checked with error message
    if version is None:
        path = Path(__file__).parent.parent / 'Schema' / study_type
        latest = max(get_immediate_subdirectories(path))

    else:
        error_msg_version(version, study_type)
        latest = version

    # Error message if the language is not correct
    error_msg_lang(lang, latest, study_type)

    # Read out the datatype and make Schema for TC equal to KT
    path_records = None
    data_header = None

    if file_type not in ['file_header', 'geo_structure']:
        error_msg_datatype(datatype, lang, latest, study_type)

        if datatype == 'TC':
            path_records = Path(__file__).parent.parent / 'Schema' / study_type / latest / lang / ('definition_record_'
                                                                                                   + 'KT' + '.csv')
            data_header = Path(__file__).parent.parent / 'Schema' / study_type / latest / lang / ('definition_record_'
                                                                                                  + 'KT' + '.csv')

        elif datatype in ['FM', 'SU', 'KT']:
            path_records = Path(__file__).parent.parent / 'Schema' / study_type / latest / lang / ('definition_record_'
                                                                                                   + datatype + '.csv')
            data_header = Path(__file__).parent.parent / 'Schema' / study_type / latest / lang / ('definition_record_'
                                                                                                  + datatype + '.csv')

    path_dict = {
        'file_header': Path(__file__).parent.parent / 'Schema' / study_type / latest / lang / 'definition_header_record'
                                                                                              '.csv',
        'geo_structure': Path(__file__).parent.parent / 'Schema' / study_type / latest / lang / 'definition_'
                                                                                                'geostructure.csv',
        'data_header': data_header,
        'data_records': path_records
    }


################################################################################################################

    # Load and print header
    if file_type == 'file_header':

        struct = pd.read_csv(path_dict.get(file_type), sep=';')
        print('Studytype (e.g. RPM) and datatype (e.g. FM) are mandatory in the header dictionary.',
              'Please pass only string values in the header dict, no column names of the dataframe.')
        print(struct.iloc[:, 1:3])

    # Load and print geo structure
    if file_type == 'geo_structure':
        struct = pd.read_csv(path_dict.get(file_type), sep=';')
        print(struct.iloc[:, 1:3])

    # Load and Print data header
    if file_type == 'data_header':
        struct = pd.read_csv(path_dict.get(file_type), sep=';')
        print(struct.iloc[:, 1:3])

    # Load and print data structure
    if file_type == 'data_records':
        struct = pd.read_csv(path_dict.get(file_type), sep=';')
        print(struct.iloc[:, 1:3])
