import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.constituency import Constituency
from app.models.election import Election

@pytest.fixture
async def sample_data(db: AsyncSession):
    """
    Create sample data for testing constituency endpoints.
    
    Creates a test election and two constituencies.
    """
    # Create a test election
    election = Election(
        name="Test Election",
        description="Test election for constituency endpoints",
        status="active",
        start_date="2025-01-01T00:00:00Z",
        end_date="2025-01-01T20:00:00Z"
    )
    db.add(election)
    await db.flush()
    
    # Create test constituencies
    constituencies = [
        Constituency(
            name="Test Constituency 1",
            code="TC001",
            description="Test constituency 1",
            election_id=election.id,
            registered_voters=10000,
            status="active",
            region="North",
            city="Test City 1"
        ),
        Constituency(
            name="Test Constituency 2",
            code="TC002",
            description="Test constituency 2",
            election_id=election.id,
            registered_voters=15000,
            status="active",
            region="South",
            city="Test City 2"
        )
    ]
    
    for constituency in constituencies:
        db.add(constituency)
    
    await db.commit()
    
    # Return created data for use in tests
    return {
        "election": election,
        "constituencies": constituencies
    }

def test_list_constituencies(client: TestClient, sample_data):
    """
    Test that the list constituencies endpoint returns a 200 status code
    and contains the expected data.
    """
    response = client.get("/api/constituencies")
    
    # Check status code
    assert response.status_code == 200
    
    # Check response structure
    data = response.json()
    assert "metadata" in data
    assert "data" in data
    
    # Check metadata
    assert "total" in data["metadata"]
    assert "page" in data["metadata"]
    assert "page_size" in data["metadata"]
    assert "pages" in data["metadata"]
    
    # Check data
    assert isinstance(data["data"], list)
    assert len(data["data"]) == 2  # We created 2 constituencies
    
    # Check first constituency data
    constituency = data["data"][0]
    assert "id" in constituency
    assert "name" in constituency
    assert "code" in constituency
    assert "election_id" in constituency
    assert "election_name" in constituency
    assert "registered_voters" in constituency
    assert "status" in constituency
    assert "created_at" in constituency
    assert "updated_at" in constituency

def test_get_constituency(client: TestClient, sample_data):
    """
    Test that the get constituency endpoint returns a 200 status code
    and contains the expected data.
    """
    # Get the first constituency ID
    constituency_id = sample_data["constituencies"][0].id
    
    response = client.get(f"/api/constituencies/{constituency_id}")
    
    # Check status code
    assert response.status_code == 200
    
    # Check constituency data
    data = response.json()
    assert data["id"] == constituency_id
    assert data["name"] == "Test Constituency 1"
    assert data["code"] == "TC001"
    assert data["description"] == "Test constituency 1"
    assert data["election_id"] == sample_data["election"].id
    assert data["election_name"] == "Test Election"
    assert data["registered_voters"] == 10000
    assert data["status"] == "active"
    assert "location" in data
    assert data["location"]["region"] == "North"
    assert data["location"]["city"] == "Test City 1"
    assert "statistics" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_get_constituency_not_found(client: TestClient):
    """
    Test that the get constituency endpoint returns a 404 status code
    when the constituency is not found.
    """
    response = client.get("/api/constituencies/9999")
    
    # Check status code
    assert response.status_code == 404
    
    # Check error response
    data = response.json()
    assert "error" in data
    assert "message" in data["error"]
    assert "Constituency with ID 9999 not found" in data["error"]["message"]

def test_list_constituencies_with_filters(client: TestClient, sample_data):
    """
    Test that the list constituencies endpoint correctly applies filters.
    """
    election_id = sample_data["election"].id
    
    # Test filtering by election_id
    response = client.get(f"/api/constituencies?election_id={election_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    
    # Test filtering by status
    response = client.get("/api/constituencies?status=active")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    
    # Test filtering by both election_id and status
    response = client.get(f"/api/constituencies?election_id={election_id}&status=active")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    
    # Test filtering with no results
    response = client.get("/api/constituencies?status=inactive")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 0
    assert data["metadata"]["total"] == 0

def test_list_constituencies_pagination(client: TestClient, sample_data):
    """
    Test that the list constituencies endpoint correctly handles pagination.
    """
    # Test page_size
    response = client.get("/api/constituencies?page_size=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["metadata"]["total"] == 2
    assert data["metadata"]["page"] == 1
    assert data["metadata"]["page_size"] == 1
    assert data["metadata"]["pages"] == 2
    
    # Test page
    response = client.get("/api/constituencies?page=2&page_size=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["metadata"]["page"] == 2