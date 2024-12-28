import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_login_rate_limit(client):
    # Test rate limiting
    for _ in range(6):  # Try 6 times (limit is 5)
        rv = client.post('/login', data={
            'username': 'test',
            'password': 'test'
        })
    assert rv.status_code == 429  # Too Many Requests

def test_sensitive_data_endpoint(client):
    rv = client.get('/sensitive-data')
    assert rv.status_code == 200
    assert 'data' in rv.get_json() 