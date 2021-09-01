import numpy as np
import pandas as pd
from functools import reduce


def write_data(_path_structure, _frame, _dict_data, _study_type, _datatype, _latest, _lang):
    """
    This function returns the data for the dat file

    Args:
        _path_structure: path to the structure file
        _frame (Pandas DataFrame): DataFrame with the values for the the geo structure
        _dict_data (Dictionary): The dictionary of the data structure
        _study_type (String): String value for the Study type e.g. 'RPM'
        _datatype (String): String value for the datatype
        _latest (String): String value for the version
        _lang (String): String value for the language

    Returns:
        1D array with a string for each line
    """

    # Read definition header record in struct. For TC read the KT file
    struct = pd.read_csv(_path_structure, sep=';')
    # Prepare output array
    _output = np.empty((len(_frame), len(struct)), dtype='U80', order='C')

    for counter, short_description in enumerate(struct.iloc[:, 2]):

        # Inserts number of 0, Record Type and data type
        if short_description == '0':
            _output[:, counter] = ''.zfill(int(struct.iloc[counter, 1]))
        # Inserts Satztyp
        elif short_description in ['Satztyp', 'Record Type']:
            if _datatype in ['SU', 'FM']:
                _output[:, counter] = '7'
            elif _datatype in ['KT', 'TC']:
                _output[:, counter] = '4'

        # Adding whitespaces by default in front
        elif short_description in _dict_data and struct.iloc[counter, 6] == 0:
            _output[:, counter] = np.char.rjust(_frame[_dict_data[short_description]].values.astype('U50'),
                                                int(struct.iloc[counter, 1]), fillchar=' ')
        # Adding leading zeros
        elif short_description in _dict_data and struct.iloc[counter, 6] == 1:
            _output[:, counter] = np.char.rjust(_frame[_dict_data[short_description]].values.astype('U50'),
                                                int(struct.iloc[counter, 1]), fillchar='0')
        # Adding leading whitespaces
        elif short_description in _dict_data and struct.iloc[counter, 6] == 2:
            _output[:, counter] = np.char.rjust(_frame[_dict_data[short_description]].values.astype('U50'),
                                                int(struct.iloc[counter, 1]), fillchar=' ')
        # Adding tailing whitespaces
        elif short_description in _dict_data and struct.iloc[counter, 6] == 3:
            _output[:, counter] = np.char.ljust(_frame[_dict_data[short_description]].values.astype('U50'),
                                                int(struct.iloc[counter, 1]), fillchar=' ')

        # Extract the sign and add leading zeros
        elif short_description in _dict_data and struct.iloc[counter, 6] == 4:
            _output[:, counter-1] = np.where((_frame[_dict_data[short_description]].values < 0).astype(str)
                                             == 'True', '-', '+')
            _output[:, counter] = np.char.rjust(np.abs(_frame[_dict_data[short_description]].values).astype('U50'),
                                                int(struct.iloc[counter, 1]), fillchar='0')
        # Inserting whitespaces where there is no value in dict
        else:
            _output[:, counter] = np.char.rjust(_output[:, counter], int(struct.iloc[counter, 1]), fillchar=' ')

    return reduce(np.char.add, _output.T)
