import pytest
from utils.extract import extract_all
from unittest.mock import patch, Mock

@patch("utils.extract.requests.get")
def test_fetching_content_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "<html><body><div class='collection-card'><h3>Test</h3></div></body></html>"
    mock_get.return_value = mock_response

    from utils.extract import scrape_page
    data = scrape_page(1)
    assert len(data) > 0

def test_extract():
    df = extract_all()
    assert not df.empty
    assert len(df) > 0  # Pastikan ada data yang diekstrak
    assert 'Title' in df.columns
    assert 'Timestamp' in df.columns