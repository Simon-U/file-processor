from file_processor.file_processor.file_encryption.encryption_file import write_header, write_geo, write_data, \
    write_data_header
from file_processor.file_processor.file_decryption.decryption_file import read_file
import numpy as np
from pathlib import Path

path_test_data = Path(__file__).parent.parent / 'Test_data' / 'fmh1212.dat'

path_dict = {
    'file_header': Path(__file__).parent.parent / 'Schema' / 'CSV' / 'v_3.7.0' / 'DE' / 'definition_header_record.csv',
    'geo_structure': Path(__file__).parent.parent / 'Schema' / 'CSV' / 'v_3.7.0' / 'DE' / 'definition_geostructure.csv',
    'data_header': Path(__file__).parent.parent / 'Schema' / 'CSV' / 'v_3.7.0' / 'DE' / ('definition_record_' + 'FM' +
                                                                                         '.csv'),
    'data_records': Path(__file__).parent.parent / 'Schema' / 'CSV' / 'v_3.7.0' / 'DE' / ('definition_data_' + 'FM' +
                                                                                          '.csv')
}

identifier_data = {
    'file_header': '0',
    'geo_structure': '1',
    'data_header': '5',
    'data_records_1': '4',
    'data_records_2': '7'
}


def test_write_header_number_rows():
    dict_head = {'Datei-Typ': 'FM',
                 'Berichtsart': "CSV"}
    assert len(write_header(path_dict.get('file_header'), dict_head, "CSV", "v_3.7.0", "DE")) == 1, \
        "Header is not only 1 line"


def test_write_header_length_string():
    dict_head = {'Datei-Typ': 'FM',
                 'Berichtsart': "CSV"}
    assert len(write_header(path_dict.get('file_header'), dict_head, "CSV", "v_3.7.0", "DE")[0]) == 140,\
        " Header length is not equal to 140"


def test_write_header_equal():
    dict_head = {
        'Berichtsart': "CSV",
        'Datei-Typ': 'FM',
        'Letzter Berichtsmonat  MM/JJJJ': '12/2012',
        'Waehrungseinheit': 'EUR',
        "Hierarchie-Kennung": "H",
        "Berichtszeitraum": "1212-1212",
        "Kundennummer": "99999",
        "Kundenname": "NEW Coorpo",
        "Anzahl Datensaetze": "81",
        "Anzahl Definitionssaetze": "1982",
        "Preisdefinition": "HAP",
        "Anzahl Level": "3"
    }
    raw_data = np.genfromtxt(path_test_data, dtype=str, delimiter=140, encoding='latin-1')
    assert write_header(path_dict.get('file_header'), dict_head, "CSV", "v_3.7.0", "DE") == raw_data[0],\
        "Written and raw data header are not equal"


def test_write_geo_length_string():
    dict_geo = {
        "Geolevel": "Geolevel",
        "Geocode": "Geocode",
        "Geo Langname": "Geo Langname",
        "Geocode_hoehere_ebene": "Geocode_hoehere_ebene",
        "Geolevel_hoehere_ebene": "Geolevel_hoehere_ebene",
        "Levelbeschreibung": "Levelbeschreibung"
    }
    df_head, df_geo, df_data_head, df_data = read_file(path_test_data, to_be_merged=False)

    # Test: The sum of identical rows from the written data to the written must be the same as the length
    # of the raw data. If not, it means some rows are not correctly printed
    assert len(write_geo(path_dict.get('geo_structure'), df_geo, dict_geo, "CSV",
                         "v_3.7.0", "DE")[0]) == 140, "Written geo data length is not 140"


def test_write_geo_equals():
    dict_geo = {
        "Geolevel": "Geolevel",
        "Geocode": "Geocode",
        "Geo Langname": "Geo Langname",
        "Geocode_hoehere_ebene": "Geocode_hoehere_ebene",
        "Geolevel_hoehere_ebene": "Geolevel_hoehere_ebene",
        "Levelbeschreibung": "Levelbeschreibung"
    }
    df_head, df_geo, df_data_head, df_data = read_file(path_test_data, to_be_merged=False)

    sel_data = np.genfromtxt(path_test_data, dtype=str, delimiter=1, encoding='latin-1')[:, 27]
    raw_data = np.genfromtxt(path_test_data, dtype=str, delimiter=140, encoding='latin-1')

    # Test: The sum of identical rows from the written data to the written must be the same as the length
    # of the raw data. If not, it means some rows are not correctly printed
    assert sum(raw_data[(sel_data == '1')] == write_geo(path_dict.get('geo_structure'), df_geo, dict_geo, "CSV",
        "v_3.7.0", "DE")) == len(raw_data[(sel_data == '1')]), "Written geo data and raw data are not equal"


def test_write_data_header_number_rows():

    dict_data_header = {
        "Gruppencode": "Z01A0",
        "Produktcode": "99999",
        "Code": "1",
        "Praeparatename": "IMSIRIN",
        "Hersteller-Langbeschreibung": "IMSHEALTH",
        "Product Registation Code": "0",
        "Pseudo-IFA-Nummer (PZN)": "8888888",
        "Herstellerkuerzel": "IMS",
        "Darreichungsform": "KAPS",
        "Packungsgroesse": "24"
    }

    df_data = read_file(path_test_data, to_be_merged=True)

    assert len(write_data_header(path_dict.get('data_header'), df_data, dict_data_header, "CSV", "FM", "v_3.7.0", "DE")
               ) == 1, "Data header is not only 1 line"


def test_write_data_header_length_string():
    dict_data_header = {
        "Gruppencode": "Gruppencode",
        "Produktcode": "99999",
        "Code": "1",
        "Praeparatename": "IMSIRIN",
        "Hersteller-Langbeschreibung": "IMSHEALTH",
        "Product Registation Code": "0",
        "Pseudo-IFA-Nummer (PZN)": "8888888",
        "Herstellerkuerzel": "IMS",
        "Darreichungsform": "KAPS",
        "Packungsgroesse": "24"
    }

    df_data = read_file(path_test_data, to_be_merged=True)

    assert len(write_data_header(path_dict.get('data_header'), df_data, dict_data_header, "CSV", "FM", "v_3.7.0", "DE")
               [0]) == 140, "Data header length is not equal to 140"


def test_write_data_header_equal():
    dict_data_header = {
        "Gruppencode": "Gruppencode",
        "Produktcode": "99999",
        "Code": "1",
        "Productname": "NEWDEVE",
        "Hersteller-Langbeschreibung": "COMPANY12",
        "Product Registation Code": "00",
        "IFA-Nummer (PZN)": "8888888",
        "Herstellerkuerzel": "NEW",
        "Darreichungsform": "KAPS",
        "Packungsgroesse": "24",
        "Check Digits PPN": "00"
    }

    df_data = read_file(path_test_data, to_be_merged=True)
    raw_data = np.genfromtxt(path_test_data, dtype=str, delimiter=140, encoding='latin-1')
    assert write_data_header(path_dict.get('data_header'), df_data, dict_data_header, "CSV", "FM", "v_3.7.0", "DE")[0] \
           == raw_data[1982], "Written data header is not equal to raw data"


def test_write_data_length_string():
    dict_data = {
        "Gruppencode": "Gruppencode",
        "Produktcode": "Produktcode",
        "Code": "Code",
        "Geolevel": "Geolevel",
        "Datentyp": "Datentyp",
        "Geocode": "Geocode",
        'Einheiten - fuer die Berichtsperiode (Einheiten von Teilmengen gerundet)':
            'Einheiten - fuer die Berichtsperiode (Einheiten von Teilmengen gerundet)',
        'Umsatz (in Cent) - fuer die Berichtsperiode': 'Umsatz (in Cent) - fuer die Berichtsperiode',
    }

    df_head, df_geo, df_data_head, df_data = read_file(path_test_data, to_be_merged=False)

    # Test: The sum of identical rows from the written data to the written must be the same as the length
    # of the raw data. If not, it means some rows are not correctly printed
    assert len(write_data(path_dict.get('data_records'), df_data, dict_data, "CSV", "FM", "v_3.7.0", "DE")[0]) == 140, \
        "Written string is not length 140"


def test_write_data_equals():
    dict_data = {
        "Gruppencode": "Gruppencode",
        "Produktcode": "Produktcode",
        "Code": "Code",
        "Geolevel": "Geolevel",
        "Datentyp": "Datentyp",
        "Geocode": "Geocode",
        'Einheiten - fuer die Berichtsperiode (Einheiten von Teilmengen gerundet)':
            'Einheiten - fuer die Berichtsperiode (Einheiten von Teilmengen gerundet)',
        'Umsatz (in Cent) - fuer die Berichtsperiode': 'Umsatz (in Cent) - fuer die Berichtsperiode',
    }

    df_head, df_geo, df_data_head, df_data = read_file(path_test_data, to_be_merged=False)

    sel_data = np.genfromtxt(path_test_data, dtype=str, delimiter=1, encoding='latin-1')[:, 27]
    raw_data = np.genfromtxt(path_test_data, dtype=str, delimiter=140, encoding='latin-1')

    # Test: The sum of identical rows from the written data to the written must be the same as the length
    # of the raw data. If not, it means some rows are not correctly printed
    assert sum(raw_data[(sel_data == '7')] == write_data(path_dict.get('data_records'), df_data, dict_data,
                                                         "CSV", "FM", "v_3.7.0", "DE")) == \
           len(raw_data[(sel_data == '7')]), "Written data is not equal to the raw data"
