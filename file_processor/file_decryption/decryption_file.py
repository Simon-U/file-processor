from pathlib import Path
from .decryption_functions import read_file_header, read_geostructure, read_data_head, read_data_records
from ..support_functions.error_msg import *
from .decryption_support_fuctions import *


def read_file(path, to_be_merged=True, study_type=None, datatype=None, version=None, lang='DE', line_len=140,
              encode='latin-1'):
    """
    The function will read the dat file in the the path
    Args:
        path (file_path)   : The path to the file which should be processed
        to_be_merged (bol) : Should data, data header and geo structure be merged or not. Default True
        study_type (string): String for the study, for example RPM. Default is none, where the study
                             is taken fro the file header
        datatype (string)  : A string for the data type. Is read from the file header (FM, SU, TC, KT)
        version (string)   : The version of the schema files. The latest will be taken if none specified.
        version (string)   : The version of the schema files. The latest will be taken if none specified.
                             Expected is a string of the example format 'v_3.7.0'
        lang (string)      : The language to be used. Default is 'DE' but 'EN' can be used
        line_len (int)     : The length of each line in the dat file. Default is 140
        encode (string)  : Default is latin-1, but can be change according to file encoding.

    Returns:
        In case of merge = True:
            * DataFrame for head line
            * DataFrame with data, data head line and geo structure merged

        In case of merge = False:
            * DataFrame for the head line
            * DataFrame for geo structure
            * DataFrame for data head line
            * DataFrame for the data
    """

    path_read_file = Path(path)
    raw_data = np.genfromtxt(path_read_file, dtype=str, encoding=encode, delimiter=line_len)
    
    # Get the value of the 27th position in each line
    select_data = np.genfromtxt(path_read_file, dtype=str, encoding=encode, delimiter=1)[:, 27]

    if study_type is None:
        study_type = raw_data[0][31:34]

    error_msg_study_type(study_type)

    # check version and if None, get the highest version
    if version is None:
        path_to_check = Path(__file__).parent.parent / 'Schema' / study_type
        latest = max(get_immediate_subdirectories(path_to_check))
    else:
        error_msg_version(version, study_type)
        latest = version

    error_msg_lang(lang, latest, study_type)

    if datatype is None:
        datatype = raw_data[0][43:45]

    # Schema for TC is equal to KT
    if datatype == 'TC':
        datatype = 'KT'

    error_msg_datatype(datatype, lang, latest, study_type)

    path_dict = {
        'file_header': Path(__file__).parent.parent / 'Schema' / study_type / latest / lang / 'definition_header_record'
                                                                                              '.csv',
        'geo_structure': Path(__file__).parent.parent / 'Schema' / study_type / latest / lang / 'definition_'
                                                                                                'geostructure.csv',
        'data_header': Path(__file__).parent.parent / 'Schema' / study_type / latest / lang / ('definition_record_'
                                                                                               + datatype + '.csv'),
        'data_records': Path(__file__).parent.parent / 'Schema' / study_type / latest / lang / ('definition_data_'
                                                                                                + datatype + '.csv')
    }

    identifier_data = {
        'file_header': '0',
        'geo_structure': '1',
        'data_header': '5',
        'data_records_1': '4',
        'data_records_2': '7'
    }

    # ------------------------------------------------------------------------------------------------------------------
    result_head = read_file_header(path_dict.get('file_header'), raw_data, select_data,
                                   identifier_data.get('file_header'), study_type, latest, lang)

    result_geo = read_geostructure(path_dict.get('geo_structure'), raw_data, select_data,
                                   identifier_data.get('geo_structure'), study_type, latest, lang)

    result_data_head = read_data_head(path_dict.get('data_header'), raw_data, select_data,
                                      identifier_data.get('data_header'), study_type, datatype, latest, lang)

    result_data = read_data_records(path_dict.get('data_records'), raw_data, select_data,
                                    (identifier_data.get('data_records_1'), identifier_data.get('data_records_2')),
                                    study_type, datatype, latest, lang)

    if not to_be_merged:
        return result_head, result_geo, result_data_head, result_data
    if to_be_merged:
        return merge_data(path_dict, result_data, result_data_head, result_geo, result_head, study_type, latest, lang,
                          datatype)
