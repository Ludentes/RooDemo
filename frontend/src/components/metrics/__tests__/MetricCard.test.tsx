import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { MetricCard } from '../MetricCard';

describe('MetricCard', () => {
  const mockMetric = {
    id: 'test-metric',
    label: 'Test Metric',
    value: 1234,
    trend: 5.5,
    trendLabel: 'vs. previous period'
  };

  it('renders the metric label', () => {
    render(<MetricCard metric={mockMetric} />);
    const labelElement = screen.getByText('Test Metric');
    expect(labelElement).toBeDefined();
  });

  it('renders the metric value', () => {
    render(<MetricCard metric={mockMetric} />);
    const valueElement = screen.getByText('1,234');
    expect(valueElement).toBeDefined();
  });

  it('renders the trend percentage', () => {
    render(<MetricCard metric={mockMetric} />);
    const trendElement = screen.getByText('5.5%');
    expect(trendElement).toBeDefined();
  });

  it('renders the trend label', () => {
    render(<MetricCard metric={mockMetric} />);
    const trendLabelElement = screen.getByText('vs. previous period');
    expect(trendLabelElement).toBeDefined();
  });

  it('renders a loading skeleton when isLoading is true', () => {
    const { container } = render(<MetricCard metric={mockMetric} isLoading={true} />);
    // Check for skeleton elements
    const skeletonElements = container.querySelectorAll('.skeleton');
    expect(skeletonElements.length).toBeGreaterThan(0);
  });

  it('handles negative trend values', () => {
    const negativeMetric = {
      ...mockMetric,
      trend: -3.2
    };
    render(<MetricCard metric={negativeMetric} />);
    const trendElement = screen.getByText('3.2%');
    expect(trendElement).toBeDefined();
  });

  it('does not render trend for zero trend value', () => {
    const zeroMetric = {
      ...mockMetric,
      trend: 0
    };
    render(<MetricCard metric={zeroMetric} />);
    // Zero trend should not be displayed
    const trendElements = screen.queryByText('0%');
    expect(trendElements).toBeNull();
  });
});