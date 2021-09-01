import numpy as np
import pandas as pd
from functools import reduce


def write_header(_path_structure, _dict_header, _study_type, _latest, _lang):
    """
    This function returns the header line for the dat file

    Args:
        _path_structure: path to the structure file
        _dict_header (Dictionary): The dictionary of the header line
        _study_type (String): String value for the study type e.g. 'RPM'
        _latest (String): String value for the version
        _lang (String): String value for the language

    Returns:
        one string value for the header line
    """

    struct = pd.read_csv(_path_structure, sep=';')

    # Prepare output array
    _output = np.empty(len(struct), dtype='U80', order='C')

    # Loop over the structure columns and insert the values defined by the dict
    for counter, short_description in enumerate(struct.iloc[:, 2]):

        # Inserts number of 0, Record Type and data type
        if short_description == '0':
            _output[counter] = ''.zfill(int(struct.iloc[counter, 1]))
        elif short_description in ['Satztyp', 'Record Type']:
            _output[counter] = '0'
        elif short_description in ['Datentyp', 'Data Type']:
            _output[counter] = '00'

        # Adding whitespaces by default in front
        elif short_description in _dict_header and struct.iloc[counter, 6] == 0:
            _output[counter] = np.char.rjust(_dict_header[short_description], int(struct.iloc[counter, 1]),
                                             fillchar=' ')
        # Adding leading zeros
        elif short_description in _dict_header and struct.iloc[counter, 6] == 1:
            _output[counter] = np.char.rjust(_dict_header[short_description], int(struct.iloc[counter, 1]),
                                             fillchar='0')
        # Adding leading whitespaces
        elif short_description in _dict_header and struct.iloc[counter, 6] == 2:
            _output[counter] = np.char.rjust(_dict_header[short_description], int(struct.iloc[counter, 1]),
                                             fillchar=' ')
        # Adding tailing whitespaces
        elif short_description in _dict_header and struct.iloc[counter, 6] == 3:
            _output[counter] = np.char.ljust(_dict_header[short_description], int(struct.iloc[counter, 1]),
                                             fillchar=' ')
        # Inserting whitespaces where there is no value in dict
        else:
            _output[counter] = np.char.rjust(_output[counter], int(struct.iloc[counter, 1]), fillchar=' ')

            # return an array where all columns are reduced into one
    return np.array([reduce(np.char.add, _output.T)])
