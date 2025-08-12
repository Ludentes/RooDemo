"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2025-08-12 09:28:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create elections table
    op.create_table(
        'elections',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('total_constituencies', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_elections_name'), 'elections', ['name'], unique=False)
    op.create_index(op.f('ix_elections_status'), 'elections', ['status'], unique=False)
    
    # Create constituencies table
    op.create_table(
        'constituencies',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('election_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('region', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('registered_voters', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('last_update_time', sa.DateTime(), nullable=True),
        sa.Column('bulletins_issued', sa.Integer(), nullable=True),
        sa.Column('votes_cast', sa.Integer(), nullable=True),
        sa.Column('participation_rate', sa.Float(), nullable=True),
        sa.Column('anomaly_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['election_id'], ['elections.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_constituencies_election_id'), 'constituencies', ['election_id'], unique=False)
    op.create_index(op.f('ix_constituencies_name'), 'constituencies', ['name'], unique=False)
    op.create_index(op.f('ix_constituencies_region'), 'constituencies', ['region'], unique=False)
    op.create_index(op.f('ix_constituencies_status'), 'constituencies', ['status'], unique=False)
    op.create_index(op.f('ix_constituencies_type'), 'constituencies', ['type'], unique=False)
    
    # Create transactions table
    op.create_table(
        'transactions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('constituency_id', sa.String(), nullable=False),
        sa.Column('block_height', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('raw_data', sqlite.JSON(), nullable=True),
        sa.Column('operation_data', sqlite.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['constituency_id'], ['constituencies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_block_height'), 'transactions', ['block_height'], unique=False)
    op.create_index(op.f('ix_transactions_constituency_id'), 'transactions', ['constituency_id'], unique=False)
    op.create_index(op.f('ix_transactions_timestamp'), 'transactions', ['timestamp'], unique=False)
    op.create_index(op.f('ix_transactions_type'), 'transactions', ['type'], unique=False)
    
    # Create alerts table
    op.create_table(
        'alerts',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('constituency_id', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('details', sqlite.JSON(), nullable=True),
        sa.Column('notes', sqlite.JSON(), nullable=True),
        sa.Column('detected_at', sa.DateTime(), nullable=False),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.Column('assigned_to', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['constituency_id'], ['constituencies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alerts_constituency_id'), 'alerts', ['constituency_id'], unique=False)
    op.create_index(op.f('ix_alerts_detected_at'), 'alerts', ['detected_at'], unique=False)
    op.create_index(op.f('ix_alerts_severity'), 'alerts', ['severity'], unique=False)
    op.create_index(op.f('ix_alerts_status'), 'alerts', ['status'], unique=False)
    op.create_index(op.f('ix_alerts_type'), 'alerts', ['type'], unique=False)
    
    # Create hourly_stats table
    op.create_table(
        'hourly_stats',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('constituency_id', sa.String(), nullable=False),
        sa.Column('hour', sa.DateTime(), nullable=False),
        sa.Column('bulletins_issued', sa.Integer(), nullable=True),
        sa.Column('votes_cast', sa.Integer(), nullable=True),
        sa.Column('transaction_count', sa.Integer(), nullable=True),
        sa.Column('bulletin_velocity', sa.Float(), nullable=True),
        sa.Column('vote_velocity', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['constituency_id'], ['constituencies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_hourly_stats_constituency_id'), 'hourly_stats', ['constituency_id'], unique=False)
    op.create_index(op.f('ix_hourly_stats_hour'), 'hourly_stats', ['hour'], unique=False)
    
    # Create file_processing_jobs table
    op.create_table(
        'file_processing_jobs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('transactions_processed', sa.Integer(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_file_processing_jobs_filename'), 'file_processing_jobs', ['filename'], unique=False)
    op.create_index(op.f('ix_file_processing_jobs_status'), 'file_processing_jobs', ['status'], unique=False)


def downgrade() -> None:
    # Drop all tables in reverse order
    op.drop_table('file_processing_jobs')
    op.drop_table('hourly_stats')
    op.drop_table('alerts')
    op.drop_table('transactions')
    op.drop_table('constituencies')
    op.drop_table('elections')