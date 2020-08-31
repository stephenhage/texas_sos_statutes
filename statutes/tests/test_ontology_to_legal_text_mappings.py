from .. import ontology_to_legal_text_mappings
from pathlib import Path
import os
import pytest

@pytest.fixture
def homedir():
    return Path.home() / "Github/texas_sos_statutes/statutes/data/"

def test_dir_exists(homedir):
    assert os.path.isdir(homedir)

@pytest.fixture
def statutes():
    return "clean_statutes_preprocessed.csv"

def test_read_data(statutes, homedir):
    assert os.path.isfile(homedir / statutes)

def test_file_has_data(statutes):
    df = ontology_to_legal_text_mappings._read_legal_data(statutes)
    assert df.shape[0] > 0

@pytest.fixture
def ontology_template():
    return "ontology_template.xlsx"

@pytest.fixture
def ontology_sheetname():
    return "Reasons"

@pytest.fixture
def ontology_header_row():
    return 1

def test_read_ontology_data(ontology_template, homedir):
    assert os.path.isfile(homedir / ontology_template)

def test_ontology_file_has_data(ontology_template, ontology_sheetname, ontology_header_row):
    df = ontology_to_legal_text_mappings._read_ontology_data(ontology_template, ontology_sheetname, header_row = ontology_header_row)
    assert df.shape[0] > 0

@pytest.fixture
def model():
    return 'bert-base-nli-mean-tokens'

def test_embedding_works(model):
    embedder = ontology_to_legal_text_mappings._create_embedder(model)
    assert embedder
