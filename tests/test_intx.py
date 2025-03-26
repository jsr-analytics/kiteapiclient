import pytest
import requests
import time
from unittest.mock import patch, Mock
from kiteclient import KiteApp, get_enctoken  # Assuming the class is in kite_app.py
import os
# You can use a mock enc_token for testing purposes
ENCTOKEN = get_enctoken(os.getenv("USERID"),os.getenv("PASSWORD"),os.getenv("TWOFA"))  # Replace with a real enc_token for actual testing

@pytest.fixture
def kite_app():
    return KiteApp(ENCTOKEN)

# Utility function to log response time
def log_response_time(response):
    response_time = response.elapsed.total_seconds()  # Get time in seconds
    print(f"Response Time: {response_time:.4f} seconds")

# Test quote function
def test_quote(kite_app):
    instruments = "RELIANCE"  # Replace with an actual instrument
    mock_response = {
        "data": {
            "RELIANCE": {"last_price": 2200, "quantity": 100}
        }
    }
    
    # Mocking the actual API request to prevent hitting the real API
    with patch.object(requests.Session, 'get', return_value=Mock(status_code=200, json=Mock(return_value=mock_response))) as mock_get:
        start_time = time.time()
        data = kite_app.quote(instruments)
        end_time = time.time()
        
        # Log the response time
        response_time = end_time - start_time
        print(f"Response Time for quote: {response_time:.4f} seconds")
        
        assert data["RELIANCE"]["last_price"] == 2200
        assert data["RELIANCE"]["quantity"] == 100

# Test profile function
def test_profile(kite_app):
    mock_response = {
        "data": {"user_id": "12345", "name": "Test User"}
    }
    
    # Mocking the actual API request to prevent hitting the real API
    with patch.object(requests.Session, 'get', return_value=Mock(status_code=200, json=Mock(return_value=mock_response))) as mock_get:
        start_time = time.time()
        data = kite_app.profile()
        end_time = time.time()
        
        # Log the response time
        response_time = end_time - start_time
        print(f"Response Time for profile: {response_time:.4f} seconds")
        
        assert data["user_id"] == "12345"
        assert data["name"] == "Test User"

# Test ltp function
def test_ltp(kite_app):
    instruments = "RELIANCE"
    mock_response = {
        "data": {
            "RELIANCE": {"ltp": 2200}
        }
    }
    
    # Mocking the actual API request to prevent hitting the real API
    with patch.object(requests.Session, 'get', return_value=Mock(status_code=200, json=Mock(return_value=mock_response))) as mock_get:
        start_time = time.time()
        data = kite_app.ltp(instruments)
        end_time = time.time()
        
        # Log the response time
        response_time = end_time - start_time
        print(f"Response Time for ltp: {response_time:.4f} seconds")
        
        assert data["RELIANCE"]["ltp"] == 2200

# Test margins function
def test_margins(kite_app):
    mock_response = {
        "data": {"equity": 100000, "commodity": 50000}
    }
    
    # Mocking the actual API request to prevent hitting the real API
    with patch.object(requests.Session, 'get', return_value=Mock(status_code=200, json=Mock(return_value=mock_response))) as mock_get:
        start_time = time.time()
        data = kite_app.margins()
        end_time = time.time()
        
        # Log the response time
        response_time = end_time - start_time
        print(f"Response Time for margins: {response_time:.4f} seconds")
        
        assert data["equity"] == 100000
        assert data["commodity"] == 50000

# Test orders function
def test_orders(kite_app):
    mock_response = {
        "data": [{"order_id": "123", "status": "COMPLETE"}]
    }
    
    # Mocking the actual API request to prevent hitting the real API
    with patch.object(requests.Session, 'get', return_value=Mock(status_code=200, json=Mock(return_value=mock_response))) as mock_get:
        start_time = time.time()
        data = kite_app.orders()
        end_time = time.time()
        
        # Log the response time
        response_time = end_time - start_time
        print(f"Response Time for orders: {response_time:.4f} seconds")
        
        assert len(data) > 0
        assert data[0]["status"] == "COMPLETE"

# Test positions function
def test_positions(kite_app):
    mock_response = {
        "data": {"positions": [{"symbol": "RELIANCE", "quantity": 100}]}
    }
    
    # Mocking the actual API request to prevent hitting the real API
    with patch.object(requests.Session, 'get', return_value=Mock(status_code=200, json=Mock(return_value=mock_response))) as mock_get:
        start_time = time.time()
        data = kite_app.positions()
        end_time = time.time()
        
        # Log the response time
        response_time = end_time - start_time
        print(f"Response Time for positions: {response_time:.4f} seconds")
        
        assert data["positions"][0]["symbol"] == "RELIANCE"
        assert data["positions"][0]["quantity"] == 100
