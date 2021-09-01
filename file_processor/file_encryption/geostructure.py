import numpy as np
import pandas as pd
from functools import reduce


def write_geo(_path_structure, _frame, _dict_geo, _study_type, _latest, _lang):
    """
    This function returns the geo structure for the dat file

    Args:
        _path_structure: path to the structure file
        _frame (Pandas DataFrame): DataFrame with the values for the the geo structure
        _dict_geo (Dictionary): The dictionary of the geo structure
        _study_type (String): String value for the Study Type e.g. 'RPM'
        _latest (String): String value for the version
        _lang (String): String value for the language

    Returns:
        1D array with a string for each line
    """

    # Read definition header record in struct
    struct = pd.read_csv(_path_structure, sep=';')

    # Prepare output array
    _output = np.empty((len(_frame), len(struct)), dtype='U80', order='C')

    # Loop over the structure columns and insert the values defined by the dict
    for counter, short_description in enumerate(struct.iloc[:, 2]):
        # Inserts number of 0, Record Type and data type
        if short_description == '0':
            _output[:, counter] = ''.zfill(int(struct.iloc[counter, 1]))
        # Inserts 1 as Satz typ
        elif short_description in ['Satztyp', 'Record Type']:
            _output[:, counter] = '1'
        elif short_description in ['Datentyp', 'Data Type']:
            _output[:, counter] = '00'

        # Adding whitespaces by default in front
        elif short_description in _dict_geo and struct.iloc[counter, 7] == 0:
            _output[counter] = np.char.rjust(_frame[_dict_geo[short_description]].values.astype('U50'),
                                             int(struct.iloc[counter, 1]), fillchar=' ')
        # Adding leading zeros
        elif short_description in _dict_geo and struct.iloc[counter, 7] == 1:
            _output[:, counter] = np.char.rjust(_frame[_dict_geo[short_description]].values.astype('U50'),
                                                int(struct.iloc[counter, 1]), fillchar='0')
        # Adding leading whitespaces
        elif short_description in _dict_geo and struct.iloc[counter, 7] == 2:
            _output[:, counter] = np.char.rjust(_frame[_dict_geo[short_description]].values.astype('U50'),
                                                int(struct.iloc[counter, 1]), fillchar=' ')

        # Special case for Geocode where the Segment with Geolevel 90 is formatted differently
        elif short_description in _dict_geo and short_description == 'Geocode' and 'Geolevel' in _dict_geo and \
                struct.iloc[counter, 7] == 3:
            _output[:, counter] = np.where(_frame[_dict_geo['Geolevel']] != 90,
                                           np.char.ljust(_frame[_dict_geo[short_description]].values.astype('U50'),
                                                         int(struct.iloc[counter, 1]), fillchar=' '),
                                           np.char.rjust(_frame[_dict_geo[short_description]].values.astype('U50'),
                                                         int(struct.iloc[counter, 1]), fillchar='0')
                                           )
        # Adding tailing whitespaces
        elif short_description in _dict_geo and struct.iloc[counter, 7] == 3:
            _output[:, counter] = np.char.ljust(_frame[_dict_geo[short_description]].values.astype('U50'),
                                                int(struct.iloc[counter, 1]), fillchar=' ')

        # Inserting whitespaces where there is no value in dict
        else:
            _output[:, counter] = np.char.rjust(_output[:, counter], int(struct.iloc[counter, 1]), fillchar=' ')
            # return an array where all columns are reduced into one
    return reduce(np.char.add, _output.T)
