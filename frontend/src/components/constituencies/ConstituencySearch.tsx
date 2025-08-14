import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';
import { useState, useEffect } from 'react';

export interface ConstituencySearchProps {
  searchQuery: string;
  onSearchChange: (query: string) => void;
  className?: string;
}

export function ConstituencySearch({
  searchQuery,
  onSearchChange,
  className,
}: ConstituencySearchProps) {
  const [query, setQuery] = useState(searchQuery);

  // Update local state when prop changes
  useEffect(() => {
    setQuery(searchQuery);
  }, [searchQuery]);

  // Debounce search input
  useEffect(() => {
    const timer = setTimeout(() => {
      if (query !== searchQuery) {
        onSearchChange(query);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [query, searchQuery, onSearchChange]);

  return (
    <div className={cn('relative', className)}>
      <Input
        type="search"
        placeholder="Search constituencies..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-full"
      />
      {query && (
        <button
          type="button"
          onClick={() => {
            setQuery('');
            onSearchChange('');
          }}
          className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
          aria-label="Clear search"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      )}
    </div>
  );
}