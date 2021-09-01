import numpy as np
import pandas as pd
from functools import reduce


def write_data_header(_path_structure, _frame, _dict_data_header, _study_type, _datatype, _latest, _lang):
    """
    This function returns the data header line for the dat file
    Args:
        _path_structure: path to the structure file
        _frame (Pandas DataFrame): DataFrame with the values for the the geo structure
        _dict_data_header (Dictionary): The dictionary of the data header line
        _study_type (String): String value for the Study Type e.g. 'RPM'
        _datatype (String): String value for the datatype
        _latest (String): String value for the version
        _lang (String): String value for the language
    Returns:
        one string value for the header line
    """

    struct = pd.read_csv(_path_structure, sep=';')
    frame_column_name_list = _frame.columns.values.tolist()

    # Prepare output array
    _output = np.empty(len(struct), dtype='U80', order='C')

    for counter, short_description in enumerate(struct.iloc[:, 2]):
        # compare if the value of the data header is in the column name list, use the values from there
        if short_description in _dict_data_header and _dict_data_header[short_description] in frame_column_name_list:
            to_insert = _frame[_dict_data_header[short_description]].unique().item()
        elif short_description in _dict_data_header:
            to_insert = _dict_data_header[short_description]

        # Inserts number of 0, Record Type and data type
        if short_description == '0':
            _output[counter] = ''.zfill(int(struct.iloc[counter, 1]))
        elif short_description in ['Satztyp', 'Record Type']:
            _output[counter] = '5'
        elif short_description in ['Datentyp', 'Data Type']:
            _output[counter] = '00'

        # Adding whitespaces by default in front
        elif short_description in _dict_data_header and struct.iloc[counter, 7] == 0:
            _output[counter] = np.char.rjust(str(to_insert), int(struct.iloc[counter, 1]), fillchar=' ')
        # Adding leading zeros
        elif short_description in _dict_data_header and struct.iloc[counter, 7] == 1:
            _output[counter] = np.char.rjust(str(to_insert), int(struct.iloc[counter, 1]), fillchar='0')
        # Adding leading whitespaces
        elif short_description in _dict_data_header and struct.iloc[counter, 7] == 2:
            _output[counter] = np.char.rjust(str(to_insert), int(struct.iloc[counter, 1]), fillchar=' ')
        # Adding tailing whitespaces
        elif short_description in _dict_data_header and struct.iloc[counter, 7] == 3:
            _output[counter] = np.char.ljust(str(to_insert), int(struct.iloc[counter, 1]), fillchar=' ')
        # Inserting whitespaces where there is no value in dict
        else:
            _output[counter] = np.char.rjust(_output[counter], int(struct.iloc[counter, 1]), fillchar=' ')
        # return an array where all columns are reduced into one
    return np.array([reduce(np.char.add, _output.T)])
