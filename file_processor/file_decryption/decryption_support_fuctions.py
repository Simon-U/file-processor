import pandas as pd
import numpy as np

from ascii_processor.ascii_support.error_msg import error_msg_merged_columns


def slicer_vectorized(array, start, end):
    """
    This function is slicing an 1D array at the positions

    Args:
        array (1D array): A 1D array of strings
        start (int) : The starting position of the slice
        end (int)   : End position of the slice (not included)

    Returns:
            * Vector with the sliced out values
    """
    b = array.view((str, 1)).reshape(len(array), -1)[:, start:end]

    return np.frombuffer(b.tobytes(), dtype=(str, end - start))


def trim_result(frame, switch_zero=True):
    """
    The function converts the all fields to strings and removes whitespace and leading 0
    In addition inserts 0, where they would be deleted because of only 0

    Args:
        frame (list): The result list is expected and converted to np.array
        switch_zero: bol true for cutting zeros
    Returns:
        frame (np.array): Returns the processed array
    """
    # Defining the list as np array
    frame = np.asarray(frame)

    # Change the datatype to character [astype('U')] and stripping the whitespace from both sides
    frame = np.char.strip(frame.astype('U'))

    # Stripping all leading 0 but make exception for cases where there is only one or two zeros
    if switch_zero:
        frame = np.where((frame == '0') | (frame == '00') | (frame == '00000'), frame, np.char.lstrip(frame, '0'))

    return frame


def change_sign(frame):
    """
    This function changes the signs of the next column according to the sign indicator '+' or '-'

    Args:
        frame (pandas Dataframe): Input is a DataFrame

    Returns:
        frame (pandas Dataframe): DataFrame with the changed signs is returned
    """
    # Iterating of the columns of the frame
    for i in range(frame.shape[1]):
        # sum over the array where ' +' or ' - " equals 0. And if the sum is 0 then execute
        if np.sum(np.where(frame.iloc[:, i].astype(str) == '+', False,
                           np.where(frame.iloc[:, i].astype(str) == '-', False, True))) == 0:
            # multiply the following row with 1 where '+' and -1 where '-'
            frame.iloc[:, i + 1] = np.where(frame.iloc[:, i] == '+', 1, -1) * frame.iloc[:, i + 1]

    return frame


def change_type(frame, _definition_structure):
    """
    This function changes the datatype for the respective columns

    Args:
        frame (pandas DataFrame): Expects a pandas DataFrame
        _definition_structure (np.array): The values from the definition files

    Returns:
        frame (pandas DataFrame): Returns the processed dataframe
    """

    # iterates of the dataframe and changes the type to integer where specified in the struct file

    for i in range(len(_definition_structure)):
        if _definition_structure[i, 3] is True and sum(frame.iloc[:, i] != '') != 0 and (frame.iloc[:, i] == '').any():
            print('Zero instead of empty was added for:', _definition_structure[i, 2])
            frame.iloc[:, i] = np.where(frame.iloc[:, i] == '', 0, frame.iloc[:, i])
            frame.iloc[:, i] = frame.iloc[:, i].astype('int64')
        elif _definition_structure[i, 3] is True and sum(frame.iloc[:, i] != '') != 0:
            frame.iloc[:, i] = frame.iloc[:, i].astype('int64')

    return frame


def merge_data(_path_dict, _data, _data_header, _geo_structure, _file_header, _study_type, _latest, _lang, _datatype):
    """
    This function merges the data

    Args:
        _path_dict: Dictionary with all the path to struct files
        _data (Pandas DataFrame): DataFrame of the data
        _data_header (Pandas DataFrame): DataFrame of the data header line
        _geo_structure (Pandas DataFrame): DataFrame of the geo structure
        _file_header (Pandas DataFrame): DataFrame of the header line
        _study_type (String) : String of the study type e.g. 'RPM'
        _latest (String)     : Version e.g 'v_3.7.0'
        _lang (String)       : Language, is 'EN' or 'DE'
        _datatype (String)   : Is FM, SU, TC or KT. Passed internally

    Returns:
        result (Pandas DataFrame): Returns the merged DataFrame only
    """

    path_structure = _path_dict.get('data_records')
    definition_structure = pd.read_csv(path_structure, sep=';')
    columns_dropped_data = definition_structure[definition_structure.iloc[:, 5].astype(str) == 'True'].iloc[:, 2]

    path_structure = _path_dict.get('data_header')
    definition_structure = pd.read_csv(path_structure, sep=';')
    columns_dropped_data_header = definition_structure[definition_structure.iloc[:, 5].astype(str) == 'True'].iloc[:, 2]

    # Only take columns the short description (column 2) for which are to be merged (column 5) is True
    merge_dataHeader_on_data = list(definition_structure[definition_structure.iloc[:, 6].astype(str) == 'True']
                                    .iloc[:, 2])
    error_msg_merged_columns(_data, 'data_records', merge_dataHeader_on_data)
    error_msg_merged_columns(_data_header, 'data_header', merge_dataHeader_on_data)

    # The structure file for the geo structure is loaded and the to_be_dropped columns are extracted
    # Also the columns on which to merge are extracted
    path_structure = _path_dict.get('geo_structure')
    definition_structure = pd.read_csv(path_structure, sep=';')
    columns_dropped_geo_structure = definition_structure[definition_structure.iloc[:, 5].astype(str) == 'True'].iloc[:, 2]

    # Only take columns the short description (column 2) for which are to be merged (column 5) is True
    merge_geoStructure_on_data = list(definition_structure[definition_structure.iloc[:, 6].astype(str) == 'True']
                                      .iloc[:, 2])
    error_msg_merged_columns(_data, 'data_records', merge_geoStructure_on_data)
    error_msg_merged_columns(_geo_structure, 'geo_structure', merge_geoStructure_on_data)

    # The structure file for the the file header is loaded and the to_be_added columns are extracted
    path_structure = _path_dict.get('file_header')
    definition_structure = pd.read_csv(path_structure, sep=';')
    columns_added = list(definition_structure[definition_structure.iloc[:, 5].astype(str) == 'True'].iloc[:, 2])

    # A left join is performed to keep all the data, unwanted columns are dropped
    # Add the values from the header in the loop
    result = pd.merge(pd.merge(_data.drop(columns=columns_dropped_data),
                               _data_header.drop(columns=columns_dropped_data_header),
                               on=merge_dataHeader_on_data, how='left'),
                      _geo_structure.drop(columns=columns_dropped_geo_structure),
                      on=merge_geoStructure_on_data, how='left')

    for i in columns_added:
        result[i] = _file_header[i].item()
    return result
