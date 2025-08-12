import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.election import Election
from app.models.constituency import Constituency

@pytest.fixture
async def sample_data(db: AsyncSession):
    """
    Create sample data for testing election endpoints.
    
    Creates three test elections with different statuses and constituencies.
    """
    # Create test elections
    elections = [
        Election(
            name="Active Election",
            description="Currently active election",
            status="active",
            start_date="2025-01-01T00:00:00Z",
            end_date="2025-01-01T20:00:00Z"
        ),
        Election(
            name="Upcoming Election",
            description="Scheduled for the future",
            status="scheduled",
            start_date="2025-02-01T00:00:00Z",
            end_date="2025-02-01T20:00:00Z"
        ),
        Election(
            name="Completed Election",
            description="Already completed election",
            status="completed",
            start_date="2024-12-01T00:00:00Z",
            end_date="2024-12-01T20:00:00Z"
        )
    ]
    
    for election in elections:
        db.add(election)
    
    await db.flush()
    
    # Create constituencies for the active election
    constituencies = [
        Constituency(
            name="District 1",
            code="D001",
            description="Northern district",
            election_id=elections[0].id,
            registered_voters=10000,
            status="active",
            region="North",
            city="Capital City"
        ),
        Constituency(
            name="District 2",
            code="D002",
            description="Southern district",
            election_id=elections[0].id,
            registered_voters=15000,
            status="active",
            region="South",
            city="Southern City"
        )
    ]
    
    for constituency in constituencies:
        db.add(constituency)
    
    await db.commit()
    
    # Return created data for use in tests
    return {
        "elections": elections,
        "constituencies": constituencies
    }

def test_list_elections(client: TestClient, sample_data):
    """
    Test that the list elections endpoint returns a 200 status code
    and contains the expected data.
    """
    response = client.get("/api/elections")
    
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
    assert len(data["data"]) == 3  # We created 3 elections
    
    # Check first election data
    election = data["data"][0]
    assert "id" in election
    assert "name" in election
    assert "description" in election
    assert "status" in election
    assert "start_date" in election
    assert "end_date" in election
    assert "constituency_count" in election
    assert "created_at" in election
    assert "updated_at" in election

def test_get_election(client: TestClient, sample_data):
    """
    Test that the get election endpoint returns a 200 status code
    and contains the expected data.
    """
    # Get the active election ID
    election_id = sample_data["elections"][0].id
    
    response = client.get(f"/api/elections/{election_id}")
    
    # Check status code
    assert response.status_code == 200
    
    # Check election data
    data = response.json()
    assert data["id"] == election_id
    assert data["name"] == "Active Election"
    assert data["description"] == "Currently active election"
    assert data["status"] == "active"
    assert "start_date" in data
    assert "end_date" in data
    assert "registered_voters" in data
    assert "constituencies" in data
    assert len(data["constituencies"]) == 2
    assert "statistics" in data
    assert "created_at" in data
    assert "updated_at" in data
    
    # Check constituency data
    constituency = data["constituencies"][0]
    assert "id" in constituency
    assert "name" in constituency
    assert "code" in constituency
    assert "registered_voters" in constituency
    assert "status" in constituency

def test_get_election_not_found(client: TestClient):
    """
    Test that the get election endpoint returns a 404 status code
    when the election is not found.
    """
    response = client.get("/api/elections/9999")
    
    # Check status code
    assert response.status_code == 404
    
    # Check error response
    data = response.json()
    assert "error" in data
    assert "message" in data["error"]
    assert "Election with ID 9999 not found" in data["error"]["message"]

def test_get_upcoming_elections(client: TestClient, sample_data):
    """
    Test that the upcoming elections endpoint returns a 200 status code
    and contains only upcoming elections.
    """
    response = client.get("/api/elections/upcoming")
    
    # Check status code
    assert response.status_code == 200
    
    # Check response structure
    data = response.json()
    assert "metadata" in data
    assert "data" in data
    
    # Check data
    assert isinstance(data["data"], list)
    assert len(data["data"]) == 1  # Only one election is upcoming
    
    # Check election data
    election = data["data"][0]
    assert election["name"] == "Upcoming Election"
    assert election["status"] == "scheduled"

def test_list_elections_with_filters(client: TestClient, sample_data):
    """
    Test that the list elections endpoint correctly applies filters.
    """
    # Test filtering by status=active
    response = client.get("/api/elections?status=active")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["name"] == "Active Election"
    
    # Test filtering by status=scheduled
    response = client.get("/api/elections?status=scheduled")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["name"] == "Upcoming Election"
    
    # Test filtering by status=completed
    response = client.get("/api/elections?status=completed")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["name"] == "Completed Election"
    
    # Test filtering with no results
    response = client.get("/api/elections?status=invalid")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 0
    assert data["metadata"]["total"] == 0

def test_list_elections_pagination(client: TestClient, sample_data):
    """
    Test that the list elections endpoint correctly handles pagination.
    """
    # Test page_size
    response = client.get("/api/elections?page_size=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["metadata"]["total"] == 3
    assert data["metadata"]["page"] == 1
    assert data["metadata"]["page_size"] == 1
    assert data["metadata"]["pages"] == 3
    
    # Test page
    response = client.get("/api/elections?page=2&page_size=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["metadata"]["page"] == 2