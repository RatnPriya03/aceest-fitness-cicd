import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that the home page loads successfully."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'ACEest Fitness & Gym Service' in rv.data

def test_health_check(client):
    """Test the API health check endpoint."""
    rv = client.get('/api/health')
    assert rv.status_code == 200
    assert rv.get_json()['status'] == 'OK'

def test_workouts_endpoint(client):
    """Test the API workouts endpoint returns JSON data."""
    rv = client.get('/api/workouts')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'Warm-up' in data