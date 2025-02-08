import pytest
import requests

# Fixture for the base URL of the API
@pytest.fixture
def api_base_url():
    return "https://webwaymark.com/api"  # Replace with your API's base URL


# Fixture for the API client (requests session)
@pytest.fixture
def api_client(api_base_url):
    session = requests.Session()
    session.base_url = api_base_url
    yield session
    session.close()