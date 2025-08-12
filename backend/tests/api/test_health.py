from fastapi.testclient import TestClient

def test_health_check(client: TestClient):
    """
    Test that the health check endpoint returns a 200 status code
    and contains the expected fields.
    """
    response = client.get("/api/health")
    
    # Check status code
    assert response.status_code == 200
    
    # Check response data
    data = response.json()
    assert "status" in data
    assert "database_connection" in data
    assert "response_time" in data
    
    # Check data types
    assert isinstance(data["status"], str)
    assert data["status"] in ["healthy", "unhealthy"]
    assert isinstance(data["database_connection"], str)
    assert isinstance(data["response_time"], str)