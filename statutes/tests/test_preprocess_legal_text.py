from .. import preprocess_legal_text
from pathlib import Path
import os
import pytest

@pytest.fixture
def homedir():
    return Path.home() / "Github/texas_sos_statutes/statutes/data/"

def test_dir_exists(homedir):
    assert os.path.isdir(homedir)

@pytest.fixture
def regulations():
    return "tx_sales_tax_regulations.csv"

@pytest.fixture
def statutes():
    return "clean_statutes.xlsx"

def test_file_exists(regulations, homedir):
    assert os.path.isfile(homedir / regulations)

@pytest.fixture
def regs_shape():
    return (81, 4)

def test_file_correct_shape_regs(regulations, regs_shape):
    df = preprocess_legal_text._open_file(regulations)
    assert df.shape == regs_shape

@pytest.fixture
def reg_col_names():
    return ['regulation', 'service_type', 'urls', 'regulation_text']

def test_clean_names_regs(regulations, reg_col_names):
    df = preprocess_legal_text._open_file(regulations)
    df = preprocess_legal_text._clean_names(df)
    assert list(df.columns) == reg_col_names

@pytest.fixture
def statutes_shape():
    return (265, 4)

def test_file_correct_shape_statutes(statutes, statutes_shape):
    df = preprocess_legal_text._open_file(statutes)
    assert df.shape == statutes_shape

@pytest.fixture
def statute_col_names():
    return ['section', 'subsection', 'section_title', 'section_text']

def test_clean_names_statutes(statutes, statute_col_names):
    df = preprocess_legal_text._open_file(statutes)
    df = preprocess_legal_text._clean_names(df)
    assert list(df.columns) == statute_col_names

@pytest.fixture
def statute_explode_shape():
    return (4365, 6)

def test_split_statute_subsections(statutes, statute_explode_shape):
    df = preprocess_legal_text._open_file(statutes)
    df = preprocess_legal_text._clean_names(df)
    df = preprocess_legal_text._split_statute_subsections(df, textcol="section_text")
    assert df.shape == statute_explode_shape

@pytest.fixture
def final_statutes_shape():
    return (4365, 3)

@pytest.fixture
def final_statutes_colnames():
    return ['citation', 'section_title',	'text']

@pytest.fixture
def final_regulations_shape():
    return (2149, 3)

@pytest.fixture
def final_regs_colnames():
    return ['regulation', 'service_type', 'urls', 'text', 'citation',]

def test_final_cleaned_data(statutes, final_statutes_colnames, final_statutes_shape):
    df = preprocess_legal_text.subsection_split_data(statutes, standard_col = None)
    assert df.shape == final_statutes_shape
    assert list(df.columns) == final_statutes_colnames