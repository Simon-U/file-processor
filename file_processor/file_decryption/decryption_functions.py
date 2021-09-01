import pandas as pd

from .decryption_support_fuctions import slicer_vectorized, trim_result, change_type, change_sign

# TODO Separate the column number out of the function, is only dependency her


def read_file_header(_path_structure, _data, _select_data, _identifier, _study_type, _latest, _lang):
    """

    Args:
        _path_structure: path to the structure file
        _data: data from loaded file
        _select_data: the selection column from the loaded file
        _identifier: identifier for file in dat
        _study_type: studytype
        _latest: version of the schema
        _lang: language

    Returns: data header

    """

    result_head = []

    definition_structure = pd.read_csv(_path_structure, sep=';').values

    # looping over the wanted values ofr the header (place 4 in the definition_structure,
    for t in range(len(definition_structure[:, 4][definition_structure[:, 4].astype(str) == 'True'])):
        result_head.append(slicer_vectorized(_data[(_select_data == _identifier)],
                                             (definition_structure[definition_structure[:, 4].astype(str) == 'True'][
                                                  t, 0] - 1),
                                             (definition_structure[definition_structure[:, 4].astype(str) == 'True'][
                                                  t, 0] - 1
                                              + definition_structure[definition_structure[:, 4].astype(str) == 'True'][
                                                  t, 1])))

    # Transform the result into pandas and save the datatype for the selection of the data definition
    result_head = trim_result(result_head, switch_zero=False)
    result_head = pd.DataFrame(result_head).T

    result_head = change_type(result_head, definition_structure[definition_structure[:, 4].astype(str) == 'True'])
    result_head = change_sign(result_head)
    result_head.columns = definition_structure[definition_structure[:, 4].astype(str) == 'True'][:, 2]

    return result_head


def read_geostructure(_path_structure, _data, _select_data, _identifier, _study_type, _latest, _lang):
    """
    Args:
        _path_structure: path to the structure file
        _data: data from loaded file
        _select_data: the selection column from the loaded file
        _identifier: identifier for file in dat
        _study_type: studytype
        _latest: version of the schema
        _lang: language

    Returns: geostructure

    """

    result_geo = []

    definition_structure = pd.read_csv(_path_structure, sep=';').values

    # looping over the wanted values ofr the header (place 4 in the definition_structure,
    for t in range(len(definition_structure[:, 4][definition_structure[:, 4].astype(str) == 'True'])):
        result_geo.append(slicer_vectorized(_data[(_select_data == _identifier)],
                                            (definition_structure[definition_structure[:, 4].astype(str) == 'True'][
                                                 t, 0] - 1),
                                            (definition_structure[definition_structure[:, 4].astype(str) == 'True'][
                                                 t, 0] - 1
                                             + definition_structure[definition_structure[:, 4].astype(str) == 'True'][
                                                 t, 1])))

    # Transform the result into pandas
    result_geo = trim_result(result_geo)
    result_geo = pd.DataFrame(result_geo).T

    result_geo = change_type(result_geo, definition_structure[definition_structure[:, 4].astype(str) == 'True'])
    result_geo = change_sign(result_geo)
    result_geo.columns = definition_structure[definition_structure[:, 4].astype(str) == 'True'][:, 2]

    return result_geo


def read_data_head(_path_structure, _data, _select_data, _identifier, _study_type, _datatype, _latest, _lang):
    """
    Args:
        _path_structure: path to the structure file
        _data: data from loaded file
        _select_data: the selection column from the loaded file
        _identifier: identifier for file in dat
        _study_type: studytype
        _datatype: datatype
        _latest: version of the schema
        _lang: language

    Returns: data header

    """
    result_data_head = []

    definition_structure = pd.read_csv(_path_structure, sep=';').values

    # looping over the wanted values ofr the header (place 4 in the definition_structure,
    for t in range(len(definition_structure[:, 4][definition_structure[:, 4].astype(str) == 'True'])):
        result_data_head.append(slicer_vectorized(_data[(_select_data == _identifier)],
                                                  (definition_structure[definition_structure[:, 4].astype(str)
                                                                        == 'True'][t, 0] - 1),
                                                  (definition_structure[definition_structure[:, 4].astype(str)
                                                                        == 'True'][t, 0] - 1
                                                   + definition_structure[definition_structure[:, 4].astype(str)
                                                                          == 'True'][t, 1]))
                                )

    # Transform the result into pandas
    result_data_head = trim_result(result_data_head)
    result_data_head = pd.DataFrame(result_data_head).T

    result_data_head = change_type(result_data_head, definition_structure[definition_structure[:, 4].astype(str) ==
                                                                          'True'])
    result_data_head = change_sign(result_data_head)
    result_data_head.columns = definition_structure[definition_structure[:, 4].astype(str) == 'True'][:, 2]

    return result_data_head


def read_data_records(_path_structure, _data, _select_data, _identifier, _study_type, _datatype, _latest, _lang):
    """
    Args:
        _path_structure: path to the structure file
        _data: data from loaded file
        _select_data: the selection column from the loaded file
        _identifier: identifier for file in dat. here tuple of two
        _study_type: studytype
        _datatype: datatype
        _latest: version of the schema
        _lang: language

    Returns: data records

    """

    # Loading the data
    identifier_1, identifier_2 = _identifier

    definition_structure = pd.read_csv(_path_structure, sep=';').values

    result_data = []

    # looping over the wanted values ofr the header (place 4 in the definition_structure,

    for t in range(len(definition_structure[:, 4][definition_structure[:, 4].astype(str) == 'True'])):
        result_data.append(slicer_vectorized(_data[(_select_data == identifier_1) | (_select_data == identifier_2)],
                                             (definition_structure[definition_structure[:, 4].astype(str) == 'True'][
                                                  t, 0] - 1),
                                             (definition_structure[definition_structure[:, 4].astype(str) == 'True'][
                                                  t, 0] - 1
                                              + definition_structure[definition_structure[:, 4].astype(str) == 'True'][
                                                  t, 1])))

    # Transform the result into pandas
    result_data = trim_result(result_data)
    result_data = pd.DataFrame(result_data).T

    result_data = change_type(result_data, definition_structure[definition_structure[:, 4].astype(str) == 'True'])
    result_data = change_sign(result_data)
    result_data.columns = definition_structure[definition_structure[:, 4].astype(str) == 'True'][:, 2]

    return result_data
