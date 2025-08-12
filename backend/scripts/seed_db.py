"""
Seed script for the Election Monitoring System.

This script populates the database with sample data for testing and development.
"""

import os
import sys
import logging
from datetime import datetime, timedelta
import random

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.database import SessionLocal, create_tables
from app.models.election import Election
from app.models.constituency import Constituency
from app.models.transaction import Transaction

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample data
ELECTION_TYPES = ["presidential", "parliamentary", "general", "local", "referendum"]
ELECTION_STATUSES = ["active", "completed", "upcoming", "scheduled"]
CONSTITUENCY_TYPES = ["urban", "rural", "suburban"]
CONSTITUENCY_STATUSES = ["active", "offline", "completed"]
TRANSACTION_TYPES = ["vote", "registration", "verification", "audit"]
TRANSACTION_STATUSES = ["completed", "pending", "failed"]
TRANSACTION_SOURCES = ["mobile", "web", "kiosk", "admin"]
REGIONS = ["North", "South", "East", "West", "Central"]
CITIES = ["Metropolis", "Riverside", "Hilltown", "Lakeside", "Valley"]

def seed_database():
    """Seed the database with sample data."""
    logger.info("Starting database seeding...")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Create tables if they don't exist
        create_tables()
        
        # Create elections
        logger.info("Creating elections...")
        elections = []
        
        # Active election (current)
        active_election = Election(
            name="2025 Presidential Election",
            country="United States",
            start_date=datetime.utcnow() - timedelta(days=2),
            end_date=datetime.utcnow() + timedelta(days=1),
            status="active",
            type="presidential",
            description="2025 United States Presidential Election",
            timezone="America/New_York",
            total_constituencies=50
        )
        db.add(active_election)
        db.flush()  # Flush to get the ID
        elections.append(active_election)
        
        # Upcoming election
        upcoming_election = Election(
            name="2026 Midterm Elections",
            country="United States",
            start_date=datetime.utcnow() + timedelta(days=180),
            end_date=datetime.utcnow() + timedelta(days=181),
            status="upcoming",
            type="parliamentary",
            description="2026 United States Midterm Elections",
            timezone="America/New_York",
            total_constituencies=435
        )
        db.add(upcoming_election)
        db.flush()
        elections.append(upcoming_election)
        
        # Completed election
        completed_election = Election(
            name="2024 Local Elections",
            country="United States",
            start_date=datetime.utcnow() - timedelta(days=100),
            end_date=datetime.utcnow() - timedelta(days=99),
            status="completed",
            type="local",
            description="2024 Local Elections",
            timezone="America/New_York",
            total_constituencies=25
        )
        db.add(completed_election)
        db.flush()
        elections.append(completed_election)
        
        # Create constituencies
        logger.info("Creating constituencies...")
        constituencies = []
        
        # For active election
        for i in range(50):
            registered_voters = random.randint(5000, 50000)
            bulletins_issued = random.randint(int(registered_voters * 0.5), registered_voters)
            votes_cast = random.randint(int(bulletins_issued * 0.9), bulletins_issued)
            
            constituency = Constituency(
                id=f"0x{i:08x}",  # Fake smart contract address
                election_id=active_election.id,
                name=f"District {i+1}",
                region=random.choice(REGIONS),
                type=random.choice(CONSTITUENCY_TYPES),
                status=random.choice(CONSTITUENCY_STATUSES),
                registered_voters=registered_voters,
                bulletins_issued=bulletins_issued,
                votes_cast=votes_cast,
                participation_rate=votes_cast / registered_voters if registered_voters > 0 else 0,
                anomaly_score=random.random() * 0.5,  # Lower anomaly scores for most
                last_update_time=datetime.utcnow()
            )
            db.add(constituency)
            db.flush()
            constituencies.append(constituency)
            
            # Add a few high anomaly constituencies
            if i % 10 == 0:
                constituency.anomaly_score = random.uniform(0.7, 0.95)
                db.add(constituency)
        
        # For upcoming election (fewer constituencies as it's not active yet)
        for i in range(10):
            registered_voters = random.randint(5000, 50000)
            
            constituency = Constituency(
                id=f"0x{i+100:08x}",
                election_id=upcoming_election.id,
                name=f"District {i+1}",
                region=random.choice(REGIONS),
                type=random.choice(CONSTITUENCY_TYPES),
                status="inactive",  # Use inactive since scheduled is not in the allowed statuses
                registered_voters=registered_voters,
                last_update_time=datetime.utcnow()
            )
            db.add(constituency)
            db.flush()
            constituencies.append(constituency)
        
        # For completed election
        for i in range(25):
            registered_voters = random.randint(5000, 50000)
            bulletins_issued = random.randint(int(registered_voters * 0.5), registered_voters)
            votes_cast = random.randint(int(bulletins_issued * 0.9), bulletins_issued)
            
            constituency = Constituency(
                id=f"0x{i+200:08x}",
                election_id=completed_election.id,
                name=f"District {i+1}",
                region=random.choice(REGIONS),
                type=random.choice(CONSTITUENCY_TYPES),
                status="completed",
                registered_voters=registered_voters,
                bulletins_issued=bulletins_issued,
                votes_cast=votes_cast,
                participation_rate=votes_cast / registered_voters if registered_voters > 0 else 0,
                anomaly_score=random.random() * 0.3,  # Lower anomaly scores for completed
                last_update_time=datetime.utcnow() - timedelta(days=99)
            )
            db.add(constituency)
            db.flush()
            constituencies.append(constituency)
        
        # Create transactions
        logger.info("Creating transactions...")
        
        # For active election constituencies
        for constituency in constituencies[:50]:
            # Create 20-50 transactions per constituency
            for _ in range(random.randint(20, 50)):
                # Most transactions in the last 24 hours
                hours_ago = random.randint(0, 48)
                timestamp = datetime.utcnow() - timedelta(hours=hours_ago)
                
                transaction = Transaction(
                    constituency_id=constituency.id,
                    block_height=random.randint(1000, 9999),
                    timestamp=timestamp,
                    type=random.choice(TRANSACTION_TYPES),
                    raw_data={"votes": random.randint(1, 100)},
                    operation_data={"processed": True}
                )
                
                db.add(transaction)
        
        # For completed election constituencies (fewer transactions)
        for constituency in constituencies[-25:]:
            # Create 10-30 transactions per constituency
            for _ in range(random.randint(10, 30)):
                # Transactions from when the election was active
                days_ago = random.randint(99, 100)
                hours_variation = random.randint(0, 24)
                timestamp = datetime.utcnow() - timedelta(days=days_ago, hours=hours_variation)
                
                transaction = Transaction(
                    constituency_id=constituency.id,
                    block_height=random.randint(1000, 9999),
                    timestamp=timestamp,
                    type=random.choice(TRANSACTION_TYPES),
                    raw_data={"votes": random.randint(1, 100)},
                    operation_data={"processed": True}
                )
                
                db.add(transaction)
        
        # Commit all changes
        db.commit()
        logger.info("Database seeding completed successfully!")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()