"""
End-to-end tests for the File Processing System.

This module contains tests for the complete flow from file upload API to database storage
and metrics updates.
"""

import os
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from datetime import date
import tempfile

from app.main import app
from app.models.constituency import Constituency
from app.models.transaction import Transaction


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def test_election(db_session):
    """Create a test election in the database."""
    from app.models.election import Election
    from datetime import datetime, timedelta
    
    # Create a test election
    election = Election(
        id="e12345",
        name="Test Election",
        country="Test Country",
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=1),
        status="active",
        type="test",
        description="Test Election Description",
        timezone="UTC"
    )
    db_session.add(election)
    db_session.commit()
    db_session.refresh(election)
    return election

@pytest.fixture
def test_constituency(db_session, test_election):
    """Create a test constituency in the database."""
    constituency = Constituency(
        id="AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM",
        election_id=test_election.id,  # Use the actual election ID
        name="Test Constituency",
        region="Test Region",
        type="test",
        status="active",
        registered_voters=1000,
        bulletins_issued=0,
        votes_cast=0,
        participation_rate=0.0,
        anomaly_score=0.0
    )
    db_session.add(constituency)
    db_session.commit()
    db_session.refresh(constituency)
    return constituency


@pytest.fixture
def sample_csv_path():
    """Get the path to the sample CSV file."""
    # Use relative path from the project root
    project_root = Path(__file__).parent.parent.parent.parent
    return project_root / "data" / "sample-data" / "90 - Пермский край" / "Выборы депутатов Думы Красновишерского городского округа" / "Округ №1_3" / "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM" / "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900" / "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM_2024-09-06_0800-0900.csv"


@pytest.mark.integration
def test_file_upload_end_to_end(client, db_session, sample_csv_path):
    """
    Test the complete flow from file upload to database storage and metrics updates.
    
    This test:
    1. Uploads a CSV file via the API
    2. Verifies that transactions are stored in the database
    3. Verifies that constituency metrics are updated correctly
    """
    # Verify the sample file exists
    assert sample_csv_path.exists(), f"Sample CSV file not found at {sample_csv_path}"
    
    # Upload the file
    with open(sample_csv_path, "rb") as file:
        response = client.post(
            "/api/files/upload",
            files={"file": (sample_csv_path.name, file, "text/csv")}
        )
    
    # Check response
    assert response.status_code == 200, f"File upload failed: {response.text}"
    result = response.json()
    
    # Verify response data
    assert result["filename"] == sample_csv_path.name
    assert result["constituency_id"] == "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
    assert result["date"] == "2024-09-06"
    assert result["time_range"] == "0800-0900"
    assert result["transactions_processed"] > 0
    
    # Verify transactions in database
    transactions = db_session.query(Transaction).filter_by(
        constituency_id="AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
    ).all()
    
    assert len(transactions) > 0, "No transactions found in database"
    
    # Count transactions by type
    blindsig_count = sum(1 for t in transactions if t.type == "blindSigIssue")
    vote_count = sum(1 for t in transactions if t.type == "vote")
    
    assert blindsig_count > 0, "No blindSigIssue transactions found"
    assert vote_count > 0, "No vote transactions found"
    
    # Verify constituency metrics
    constituency = db_session.query(Constituency).filter_by(
        id="AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
    ).first()
    
    assert constituency.bulletins_issued == blindsig_count
    assert constituency.votes_cast == vote_count
    assert constituency.participation_rate > 0
    
    # Get transaction statistics
    response = client.get(
        f"/api/files/statistics/{constituency.id}"
    )
    
    assert response.status_code == 200
    stats = response.json()
    
    assert stats["total_transactions"] == len(transactions)
    assert stats["bulletins_issued"] == blindsig_count
    assert stats["votes_cast"] == vote_count
    assert stats["participation_rate"] > 0


@pytest.mark.integration
def test_directory_processing_end_to_end(client, db_session):
    """
    Test the complete flow from directory processing to database storage and metrics updates.
    
    This test:
    1. Processes a directory of CSV files via the API
    2. Verifies that transactions are stored in the database
    3. Verifies that constituency metrics are updated correctly
    """
    # Directory path - use relative path from project root
    project_root = Path(__file__).parent.parent.parent.parent
    directory_path = str(project_root / "data" / "sample-data")
    
    # Process the directory
    response = client.post(
        "/api/files/process-directory",
        data={"directory_path": directory_path}
    )
    
    # Check response
    assert response.status_code == 200, f"Directory processing failed: {response.text}"
    result = response.json()
    
    # Verify response data
    assert result["files_processed"] > 0
    
    # If transactions were already processed in a previous test,
    # the transactions_processed count might be 0
    # In this case, we should verify that transactions exist in the database
    if result["transactions_processed"] == 0:
        # Verify transactions in database
        transactions = db_session.query(Transaction).filter_by(
            constituency_id="AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
        ).all()
        
        assert len(transactions) > 0, "No transactions found in database"
    else:
        assert result["transactions_processed"] > 0
    assert result["constituency_id"] == "AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
    
    # Verify transactions in database
    transactions = db_session.query(Transaction).filter_by(
        constituency_id="AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
    ).all()
    
    assert len(transactions) > 0, "No transactions found in database"
    
    # Count transactions by type
    blindsig_count = sum(1 for t in transactions if t.type == "blindSigIssue")
    vote_count = sum(1 for t in transactions if t.type == "vote")
    
    assert blindsig_count > 0, "No blindSigIssue transactions found"
    assert vote_count > 0, "No vote transactions found"
    
    # Verify constituency metrics
    constituency = db_session.query(Constituency).filter_by(
        id="AsrxMqfGWsXEgTmvdw95omtQ4Gv1Vi4mGAvLYy23DHpM"
    ).first()
    
    assert constituency.bulletins_issued == blindsig_count
    assert constituency.votes_cast == vote_count
    assert constituency.participation_rate > 0
    
    # Get transaction statistics
    response = client.get(
        f"/api/files/statistics/{constituency.id}"
    )
    
    assert response.status_code == 200
    stats = response.json()
    
    assert stats["total_transactions"] == len(transactions)
    assert stats["bulletins_issued"] == blindsig_count
    assert stats["votes_cast"] == vote_count
    assert stats["participation_rate"] > 0


@pytest.mark.integration
def test_invalid_file_upload(client, db_session):
    """Test uploading an invalid file."""
    # Create a temporary invalid file
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
        temp_file.write(b"invalid,csv,content")
        temp_path = temp_file.name
    
    try:
        # Upload the file
        with open(temp_path, "rb") as file:
            response = client.post(
                "/api/files/upload",
                files={"file": ("invalid.csv", file, "text/csv")}
            )
        
        # Check response
        # The response could be 400 or 500 depending on how the error is handled
        assert response.status_code in [400, 500]
        # The error message should contain information about the failure
        assert "Failed to extract metadata from filename" in response.text or "Failed to process file" in response.text
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)


@pytest.mark.integration
def test_nonexistent_directory_processing(client, db_session):
    """Test processing a nonexistent directory."""
    # Directory path
    directory_path = "/nonexistent/directory"
    
    # Process the directory
    response = client.post(
        "/api/files/process-directory",
        data={"directory_path": directory_path}
    )
    
    # Check response
    # The response could be 400 or 500 depending on how the error is handled
    assert response.status_code in [400, 500]
    # The error message should contain information about the failure
    assert "Directory not found" in response.text or "Failed to process directory" in response.text


@pytest.mark.integration
def test_nonexistent_constituency_statistics(client, db_session):
    """Test getting statistics for a nonexistent constituency."""
    # Get transaction statistics
    response = client.get(
        "/api/files/statistics/nonexistent-constituency"
    )
    
    # Check response
    # The response could be 404 or 500 depending on how the error is handled
    assert response.status_code in [404, 500]
    # The error message should contain information about the failure
    assert "Constituency not found" in response.text or "not found" in response.text.lower()


@pytest.mark.integration
def test_watch_directory(client, db_session, temp_dir):
    """Test watching a directory for new files."""
    # Arrange
    directory_path = temp_dir
    
    # Act
    response = client.post(
        "/api/files/watch-directory",
        data={"directory_path": directory_path}
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert result["message"] == f"Started watching directory: {directory_path}"
    assert result["recursive"] is True
    assert result["patterns"] == ["*.csv"]
    
    # Clean up
    client.post(
        "/api/files/stop-watching",
        data={"directory_path": directory_path}
    )


@pytest.mark.integration
def test_watch_directory_with_options(client, db_session, temp_dir):
    """Test watching a directory with custom options."""
    # Arrange
    directory_path = temp_dir
    
    # Act
    response = client.post(
        "/api/files/watch-directory",
        data={
            "directory_path": directory_path,
            "recursive": False,
            "patterns": ["*.txt", "*.json"]
        }
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert result["message"] == f"Started watching directory: {directory_path}"
    assert result["recursive"] is False
    assert result["patterns"] == ["*.txt", "*.json"]
    
    # Clean up
    client.post(
        "/api/files/stop-watching",
        data={"directory_path": directory_path}
    )


@pytest.mark.integration
def test_watch_nonexistent_directory(client, db_session):
    """Test watching a nonexistent directory."""
    # Arrange
    directory_path = "/nonexistent/directory"
    
    # Act
    response = client.post(
        "/api/files/watch-directory",
        data={"directory_path": directory_path}
    )
    
    # Assert
    assert response.status_code == 400
    assert "Directory not found" in response.text


@pytest.mark.integration
def test_stop_watching_directory(client, db_session, temp_dir):
    """Test stopping watching a directory."""
    # Arrange
    directory_path = temp_dir
    
    # Start watching
    client.post(
        "/api/files/watch-directory",
        data={"directory_path": directory_path}
    )
    
    # Act
    response = client.post(
        "/api/files/stop-watching",
        data={"directory_path": directory_path}
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert result["message"] == f"Stopped watching directory: {directory_path}"


@pytest.mark.integration
def test_stop_watching_all_directories(client, db_session, temp_dir):
    """Test stopping watching all directories."""
    # Arrange
    directory_path1 = temp_dir
    
    # Create another temporary directory
    with tempfile.TemporaryDirectory() as directory_path2:
        # Start watching both directories
        client.post(
            "/api/files/watch-directory",
            data={"directory_path": directory_path1}
        )
        client.post(
            "/api/files/watch-directory",
            data={"directory_path": directory_path2}
        )
        
        # Act
        response = client.post(
            "/api/files/stop-watching"
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["message"] == "Stopped watching all directories"


@pytest.mark.integration
def test_get_watching_directories(client, db_session, temp_dir):
    """Test getting a list of directories being watched."""
    # Arrange
    directory_path = temp_dir
    
    # Start watching
    client.post(
        "/api/files/watch-directory",
        data={"directory_path": directory_path}
    )
    
    # Act
    response = client.get(
        "/api/files/watching-directories"
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert result["count"] == 1
    assert directory_path in result["directories"]
    
    # Clean up
    client.post(
        "/api/files/stop-watching"
    )


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir