import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { ConstituencyCard } from '../ConstituencyCard';

describe('ConstituencyCard', () => {
  const mockConstituency = {
    id: 'constituency-1',
    name: 'Test Constituency',
    code: 'TC-001',
    region_id: 'region-1',
    region_name: 'Test Region',
    election_id: 'election-1',
    registered_voters: 10000,
    bulletins_issued: 7500,
    votes_cast: 7000,
    transaction_count: 15000,
    participation_rate: 70.0,
    anomaly_count: 2,
    last_activity: '2025-01-01T12:00:00Z'
  };

  it('renders the constituency name', () => {
    render(<ConstituencyCard constituency={mockConstituency} />);
    const nameElement = screen.getByText('Test Constituency');
    expect(nameElement).toBeDefined();
  });

  it('renders the region name', () => {
    render(<ConstituencyCard constituency={mockConstituency} />);
    const regionElement = screen.getByText('Test Region');
    expect(regionElement).toBeDefined();
  });

  it('renders the registered voters count', () => {
    render(<ConstituencyCard constituency={mockConstituency} />);
    const votersElement = screen.getByText('10,000');
    expect(votersElement).toBeDefined();
  });

  it('renders the participation rate', () => {
    render(<ConstituencyCard constituency={mockConstituency} />);
    const rateElement = screen.getByText('70.0%');
    expect(rateElement).toBeDefined();
  });

  it('renders the transaction count', () => {
    render(<ConstituencyCard constituency={mockConstituency} />);
    const transactionsElement = screen.getByText('15,000');
    expect(transactionsElement).toBeDefined();
  });

  it('renders the anomaly count', () => {
    render(<ConstituencyCard constituency={mockConstituency} />);
    const anomalyElement = screen.getByText('2');
    expect(anomalyElement).toBeDefined();
  });

  it('renders a loading skeleton when isLoading is true', () => {
    const { container } = render(<ConstituencyCard constituency={mockConstituency} isLoading={true} />);
    const skeletonElements = container.querySelectorAll('.skeleton');
    expect(skeletonElements.length).toBeGreaterThan(0);
  });

  it('calls onClick handler when clicked', () => {
    const handleClick = vi.fn();
    render(<ConstituencyCard constituency={mockConstituency} onClick={handleClick} />);
    
    const card = screen.getByText('Test Constituency').closest('.card');
    if (card) {
      fireEvent.click(card);
      expect(handleClick.mock.calls.length).toBe(1);
    } else {
      // If we can't find the card by class, try to find it by role
      const cardElement = screen.getByRole('article');
      fireEvent.click(cardElement);
      expect(handleClick.mock.calls.length).toBe(1);
    }
  });
});