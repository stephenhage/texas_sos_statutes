from .. import statute_scrape
import pytest

@pytest.fixture
def url():
    return "https://texreg.sos.state.tx.us/public/readtac$ext.ViewTAC?tac_view=5&ti=34&pt=1&ch=3&sch=O&rl=Y"

def test_is_connected(url):
    assert statute_scrape.get_first_page(url).status_code == 200

def test_get_first_page_not_empty(url):
    soup = statute_scrape.get_first_page_tags(url)
    assert len(soup) > 0

def test_get_table_and_regs_type(url):
    assert statute_scrape.get_table_regs_and_type(url).shape[0] == 81
    assert statute_scrape.get_table_regs_and_type(url).shape[1] == 2

def test_list_of_links_correct_len(url):
    assert len(statute_scrape.get_list_of_links(url)) == 81

def test_is_cont(url):
    assert statute_scrape.get_cont(url) is None

def test_regs_table_with_links(url):
    assert statute_scrape.regs_table_with_links(url).shape == (81, 3)

def test_get_all_text(url):
    assert len(statute_scrape.get_all_text(url)) == 81