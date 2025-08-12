import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.election import Election
from app.models.constituency import Constituency
from app.models.transaction import Transaction
from datetime import datetime, timedelta

@pytest.fixture
async def sample_data(db: AsyncSession):
    """
    Create sample data for testing dashboard endpoints.
    
    Creates elections, constituencies, and transactions.
    """
    # Create test elections
    active_election = Election(
        name="Active Election",
        description="Currently active election",
        status="active",
        start_date=datetime.utcnow().isoformat(),
        end_date=(datetime.utcnow() + timedelta(hours=12)).isoformat()
    )
    db.add(active_election)
    
    inactive_election = Election(
        name="Inactive Election",
        description="Inactive election",
        status="completed",
        start_date=(datetime.utcnow() - timedelta(days=30)).isoformat(),
        end_date=(datetime.utcnow() - timedelta(days=29)).isoformat()
    )
    db.add(inactive_election)
    
    await db.flush()
    
    # Create constituencies
    active_constituencies = [
        Constituency(
            name="Active District 1",
            code="AD001",
            description="Active district 1",
            election_id=active_election.id,
            registered_voters=10000,
            status="active",
            region="North",
            city="Capital City"
        ),
        Constituency(
            name="Active District 2",
            code="AD002",
            description="Active district 2",
            election_id=active_election.id,
            registered_voters=15000,
            status="active",
            region="South",
            city="Southern City"
        )
    ]
    
    inactive_constituency = Constituency(
        name="Inactive District",
        code="ID001",
        description="Inactive district",
        election_id=inactive_election.id,
        registered_voters=12000,
        status="inactive",
        region="East",
        city="Eastern City"
    )
    
    for constituency in active_constituencies:
        db.add(constituency)
    db.add(inactive_constituency)
    
    await db.flush()
    
    # Create transactions
    recent_time = datetime.utcnow() - timedelta(hours=1)
    old_time = datetime.utcnow() - timedelta(days=2)
    
    # Recent transactions (within 24 hours)
    recent_transactions = [
        Transaction(
            constituency_id=active_constituencies[0].id,
            timestamp=recent_time.isoformat(),
            bulletins_issued=100,
            votes_cast=95,
            valid_votes=90,
            invalid_votes=5,
            source="polling_station"
        ),
        Transaction(
            constituency_id=active_constituencies[1].id,
            timestamp=recent_time.isoformat(),
            bulletins_issued=150,
            votes_cast=145,
            valid_votes=140,
            invalid_votes=5,
            source="polling_station"
        )
    ]
    
    # Old transaction (more than 24 hours ago)
    old_transaction = Transaction(
        constituency_id=inactive_constituency.id,
        timestamp=old_time.isoformat(),
        bulletins_issued=200,
        votes_cast=190,
        valid_votes=185,
        invalid_votes=5,
        source="polling_station"
    )
    
    for transaction in recent_transactions:
        db.add(transaction)
    db.add(old_transaction)
    
    await db.commit()
    
    # Return created data for use in tests
    return {
        "active_election": active_election,
        "inactive_election": inactive_election,
        "active_constituencies": active_constituencies,
        "inactive_constituency": inactive_constituency,
        "recent_transactions": recent_transactions,
        "old_transaction": old_transaction
    }

def test_get_dashboard_summary(client: TestClient, sample_data):
    """
    Test that the dashboard summary endpoint returns a 200 status code
    and contains the expected data.
    """
    response = client.get("/api/dashboard/summary")
    
    # Check status code
    assert response.status_code == 200
    
    # Check response data
    data = response.json()
    
    # Check that all required fields are present
    assert "active_elections" in data
    assert "total_constituencies" in data
    assert "active_constituencies" in data
    assert "recent_transactions" in data
    
    # Check values
    assert data["active_elections"] == 1  # One active election
    assert data["total_constituencies"] == 3  # Three total constituencies
    assert data["active_constituencies"] == 2  # Two active constituencies
    assert data["recent_transactions"] == 2  # Two recent transactions
    
    # Check data types
    assert isinstance(data["active_elections"], int)
    assert isinstance(data["total_constituencies"], int)
    assert isinstance(data["active_constituencies"], int)
    assert isinstance(data["recent_transactions"], int)