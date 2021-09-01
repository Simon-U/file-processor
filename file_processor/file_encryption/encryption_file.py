import pandas as pd
import numpy as np
from pathlib import Path

from .file_header import write_header
from .geostructure import write_geo
from .data_header import write_data_header
from .data_records import write_data

from ..support_functions.error_msg import *


def write_file(folder, filename, frame, dict_header, geo_frame=None, dict_geo=None, dict_data_header=None,
               dict_data=None, version=None, lang='DE', encode='latin-1'):
    """
    This function process the input and writes it to the file
    Args:
        folder (String): String for the existing directory path to write output file to.
        filename (String): Output file name - no need to put ".dat".
        frame (Pandas DataFrame): The input dataframe
        dict_header (Dictionary): The dictionary for the header.
                                  The values for study type and datatype have to be passed here
        geo_frame (Pandas DataFrame): Data Frame with the geo structure to be passed.
        dict_geo (Dictionary): Default None. The dictionary for the geo structer,
                                if none is passed than no geo structure is written.
        dict_data_header (Dictionary): Default None. The dictionary for the data header,
                                if none is passed than no dict_data_header is written.
        dict_data (Dictionary): Default None. The dictionary for the data,
                                if none is passed than no data is written.
        version (String): Default None. If none is passed, than the latest is taken.
        lang (String): Default is 'DE'. Currently 'EN' is also supported.
        encode (string): Default value is latin-1
    Returns:
        result_end (numpy array): write result_end to file in folder and message is printed
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Check for all necessary information and raise error if not there

    # Raise error if geo_frame is passed but no dict_geo
    if geo_frame is not None and dict_geo is None:
        raise ValueError('You passed a geo structure but not the dict_geo. Please pass dict_geo as well')

    # Read out the study_type
    if lang == 'DE':
        study_type = dict_header['Berichtsart']
    elif lang == 'EN':
        study_type = dict_header['Report Type']
    else:
        raise ValueError('Language %s not accepted. Following languages are possible DE or EN' % lang)

    # Check study type. And if not found then give error message
    error_msg_study_type(study_type)

    # check version and if None, get the highest version
    # If the version is passed manually then it will be checked with error message
    if version is None:
        path_to_check = Path(__file__).parent.parent / 'Schema' / study_type
        latest = max(get_immediate_subdirectories(path_to_check))
    else:
        error_msg_version(version, study_type)
        latest = version

    # Error message if the language is not correct
    error_msg_lang(lang, latest, study_type)

    # Read out the datatype and make Schema for TC equal to KT
    datatype = None
    if lang == 'DE':
        datatype = dict_header['Datei-Typ']
    if lang == 'EN':
        datatype = dict_header['File Type']
    if datatype == 'TC':
        error_msg_datatype('KT', lang, latest, study_type)
    else:
        error_msg_datatype(datatype, lang, latest, study_type)

    if datatype == 'TC':
        path_records = Path(__file__).parent.parent / 'Schema' / study_type / latest / lang / ('definition_record_'
                                                                                               + 'KT' + '.csv')
        data_header = Path(__file__).parent.parent / 'Schema' / study_type / latest / lang / ('definition_record_'
                                                                                              + 'KT' + '.csv')

    else:
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

    # ------------------------------------------------------------------------------------------------------------------

    # generate list of merge columns and values
    struct = pd.read_csv(path_dict.get('data_records'), sep=';')
    list_merge_columns_structure = struct.iloc[:, 2][struct.iloc[:, 6].astype(str) == 'True'].tolist()
    list_merge_columns_dictionary = list(dict_data_header.keys())
    list_merge_columns = list(set(list_merge_columns_structure).intersection(set(list_merge_columns_dictionary)))

    # Selecting the unique values of list_merge-columns from the data
    column_values = frame[list_merge_columns].drop_duplicates().reset_index().drop(columns=['index'])

    # ------------------------------------------------------------------------------------------------------------------
    # Write data header

    if geo_frame is not None and dict_geo is not None:
        count_definition = str(len(geo_frame.filter(items=dict_geo.values()).drop_duplicates())+1)
    elif dict_geo is not None:
        count_definition = str(len(frame.filter(items=dict_geo.values()).drop_duplicates())+1)

    if lang == 'DE':
        if 'Anzahl Datensaetze' not in dict_header.keys():
            dict_header['Anzahl Datensaetze'] = str(len(frame) + len(column_values))
        if 'Anzahl Definitionssaetze' not in dict_header.keys():
            dict_header['Anzahl Definitionssaetze'] = count_definition
    elif lang == 'EN':
        if 'Count of Data Records' not in dict_header.keys():
            dict_header['Count of Data Records'] = str(len(frame) + len(column_values))
        if 'Count of Definition Records' not in dict_header.keys():
            dict_header['Count of Definition Records'] = count_definition

    # Write the header line. It is mandatory, since study_type is derived there
    result_end = write_header(path_dict.get('file_header'), dict_header, study_type, latest, lang)

    # ------------------------------------------------------------------------------------------------------------------
    # Write the geo structure if a geo frame and dict is given

    if geo_frame is not None and dict_geo is not None:
        # Check the values for geo level and gecode
        error_msg_geolevel(dict_geo)

        result = write_geo(path_dict.get('geo_structure'), geo_frame.filter(items=dict_geo.values()).drop_duplicates(),
                           dict_geo, study_type, latest, lang)
        result_end = np.concatenate((result_end, result))
    # Write the geo structure if only a geo dict is given
    elif dict_geo is not None:
        result = write_geo(path_dict.get('geo_structure'), frame.filter(items=dict_geo.values()).drop_duplicates(),
                           dict_geo, study_type, latest, lang)
        result_end = np.concatenate((result_end, result))

    # ------------------------------------------------------------------------------------------------------------------
    # Write data header with corresponding data

    # Select data for header/data combination
    # Here we iterate over the combination of the unique data rows
    for i in range(len(column_values)):
        selection = frame.copy()

        # Selecting data from the unique data row with all columns from list_merge_columns
        for t, column in enumerate(list_merge_columns):
            selection = selection[:][selection[column] == column_values[column][i]]

        # ----------------------------------------------------------------------------------------------------------
        # Write the data header if a data header dict is given

        if bool(dict_data_header):
            result = write_data_header(path_dict.get('data_header'), selection, dict_data_header, study_type, datatype,
                                       latest, lang)
            result_end = np.concatenate((result_end, result))

        # ----------------------------------------------------------------------------------------------------------
        # Write the data if a data dict is given

        if bool(dict_data):
            result = write_data(path_dict.get('data_records'), selection, dict_data, study_type, datatype, latest, lang)
            result_end = np.concatenate((result_end, result))

    # ------------------------------------------------------------------------------------------------------------------

    # Save the file
    folder = Path(folder)
    full_path = folder / (filename + ".dat")
    np.savetxt(full_path, result_end, fmt='%s', encoding=encode)

    # Print message
    print('The file was successfully writen to: ' + str(full_path))
