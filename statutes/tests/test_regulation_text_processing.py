from .. import regulation_text_processing
import os
import pandas as pd
import pytest

@pytest.fixture
def statutes_file():
    return "/Users/stephenhage/Github/texas_sos_statutes/statutes/data/statutes_text.txt"

def test_file_exists(statutes_file):
    assert os.path.isfile(statutes_file)

def _open_file(statutes_file):
    return regulation_text_processing._open_file(statutes_file)

def test_file_not_blank(statutes_file):
    statutes = _open_file(statutes_file)
    assert len(statutes) > 0

def test_matches_exist(statutes_file):
    assert len(regulation_text_processing._extract_matches(statutes_file)) > 0

@pytest.fixture
def statutes_shape():
    return (265, 2)

def test_dataframe_can_be_made(statutes_file, statutes_shape):
    df = regulation_text_processing.make_dataframe_statutes(statutes_file)
    assert df.shape == statutes_shape

@pytest.fixture
def sprdsht():
    return "/Users/stephenhage/Github/texas_sos_statutes/statutes/data/raw_statutes.xlsx"

@pytest.fixture
def df(sprdsht):
    return pd.read_excel(sprdsht)

def test_remove_sec_from_section(df):
    out_df = regulation_text_processing._remove_sec_from_section(df)
    assert out_df.loc[out_df.Section.str.contains("Sec. "), ].shape == (0, 2)

def test_split_section(df):
    out_df = regulation_text_processing._split_section(df)
    assert out_df.shape == (265, 3)

def test_split_text_header(df):
    out_df = regulation_text_processing._split_text_header(df)
    assert out_df.shape == (265, 4)