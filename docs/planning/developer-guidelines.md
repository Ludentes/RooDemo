# Election Monitoring System - Developer Guidelines

## Code Quality Standards

### General Principles
- **Readability**: Code should be self-documenting and clear
- **Consistency**: Follow established patterns within the project
- **Simplicity**: Prefer simple solutions over complex ones
- **Testability**: Write code that can be easily tested
- **Documentation-First**: Always start with clear requirements before coding

### Error Handling

#### Backend (Python/FastAPI)
```python
# Proper error handling in FastAPI
from fastapi import HTTPException, status

# For expected errors with user feedback
def get_constituency(constituency_id: str, db: Session):
    constituency = db.query(Constituency).filter(Constituency.id == constituency_id).first()
    if not constituency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Constituency with ID {constituency_id} not found"
        )
    return constituency

# For background tasks and services
try:
    process_file(file_path)
except FileNotFoundError:
    logger.error(f"File not found: {file_path}")
    # Handle gracefully
except Exception as e:
    logger.exception(f"Unexpected error processing file: {e}")
    # Fallback behavior
```

#### Frontend (TypeScript/React)
```typescript
// API error handling
const fetchConstituencyDetail = async (id: string) => {
  try {
    const response = await apiClient.get<ConstituencyDetail>(`/constituencies/${id}`);
    return response;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      // Handle specific HTTP errors
      if (error.response?.status === 404) {
        throw new Error(`Constituency ${id} not found`);
      }
      throw new Error(`API error: ${error.response?.data.detail || error.message}`);
    }
    // Handle unexpected errors
    console.error('Unexpected error:', error);
    throw new Error('An unexpected error occurred');
  }
};

// Component error boundaries
import { ErrorBoundary } from 'react-error-boundary';

const ErrorFallback = ({ error, resetErrorBoundary }) => (
  <div role="alert" className="error-container">
    <h2>Something went wrong:</h2>
    <pre>{error.message}</pre>
    <button onClick={resetErrorBoundary}>Try again</button>
  </div>
);

// Usage
<ErrorBoundary FallbackComponent={ErrorFallback}>
  <ConstituencyDetail id={constituencyId} />
</ErrorBoundary>
```

### Testing Standards
- **Unit Tests**: Test individual functions and components
  - Backend: pytest for Python code
  - Frontend: Jest/React Testing Library for React components
- **Integration Tests**: Test component interactions
  - Backend: FastAPI TestClient
  - Frontend: Mock API responses and test state updates
- **End-to-End Tests**: Test complete user workflows
  - Cypress for critical user journeys
- **Minimum Coverage**: 
  - Backend: 80% code coverage
  - Frontend: 70% code coverage

### Code Organization

#### Backend Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── dependencies.py      # FastAPI dependencies
│   │
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   ├── database.py      # Database connection
│   │   └── schemas.py       # Pydantic models
│   │
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── file_processor.py
│   │   ├── metrics_calculator.py
│   │   ├── anomaly_detector.py
│   │   └── alert_manager.py
│   │
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── dashboard.py
│   │   ├── constituencies.py
│   │   ├── alerts.py
│   │   └── files.py
│   │
│   ├── core/                # Core functionality
│   │   ├── __init__.py
│   │   ├── background_tasks.py
│   │   ├── file_watcher.py
│   │   └── websocket_manager.py
│   │
│   └── utils/               # Utilities
│       ├── __init__.py
│       ├── csv_parser.py
│       └── validators.py
│
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_api/
│   ├── test_services/
│   └── test_utils/
│
└── alembic/                 # Database migrations
    ├── versions/
    └── alembic.ini
```

#### Frontend Structure
```
frontend/
├── public/                  # Static assets
│   ├── index.html
│   └── favicon.ico
│
├── src/
│   ├── components/          # React components
│   │   ├── ui/              # Reusable UI components
│   │   ├── dashboard/       # Dashboard components
│   │   ├── constituencies/  # Constituency components
│   │   └── alerts/          # Alert components
│   │
│   ├── stores/              # Zustand state management
│   │   ├── types.ts         # TypeScript interfaces
│   │   ├── dashboardStore.ts
│   │   ├── constituencyStore.ts
│   │   ├── alertStore.ts
│   │   └── appStore.ts
│   │
│   ├── services/            # API services
│   │   ├── apiClient.ts     # Base API client
│   │   ├── dashboardService.ts
│   │   ├── constituencyService.ts
│   │   └── alertService.ts
│   │
│   ├── pages/               # Page components
│   │   ├── Dashboard.tsx
│   │   ├── ConstituencyDetail.tsx
│   │   └── AlertManagement.tsx
│   │
│   ├── utils/               # Utility functions
│   │   ├── formatters.ts
│   │   ├── validators.ts
│   │   └── hooks.ts
│   │
│   ├── App.tsx              # Main application component
│   ├── main.tsx             # Application entry point
│   └── vite-env.d.ts        # Vite type declarations
│
├── tests/                   # Test suite
│   ├── components/
│   ├── stores/
│   └── services/
│
└── vite.config.ts           # Vite configuration
```

### Documentation Requirements
- **Function Documentation**: 
  - Python: Docstrings for all public functions
  - TypeScript: JSDoc comments for functions and interfaces
- **API Documentation**: 
  - FastAPI automatic OpenAPI documentation
  - Additional context and examples for complex endpoints
- **README**: 
  - Keep project README current with setup instructions
  - Document environment variables and configuration
- **Architecture Decisions**: 
  - Document significant choices in `/docs/planning/`
  - Update data model documentation when schema changes

### Performance Guidelines

#### Backend Performance
- **Database Optimization**:
  - Use appropriate indexes for query patterns
  - Limit query results with pagination
  - Use SQLAlchemy query optimization techniques
- **File Processing**:
  - Process large files in chunks
  - Use background tasks for long-running operations
  - Implement caching for frequently accessed data
- **API Optimization**:
  - Use async endpoints for I/O-bound operations
  - Implement response compression
  - Return only necessary fields

#### Frontend Performance
- **React Optimization**:
  - Use React.memo for expensive components
  - Implement virtualization for long lists
  - Lazy load components and routes
- **State Management**:
  - Keep Zustand stores focused and minimal
  - Use selectors to prevent unnecessary rerenders
  - Implement optimistic UI updates
- **Network Optimization**:
  - Implement request caching
  - Use WebSocket for real-time updates
  - Batch API requests when possible

### Security Practices
- **Input Validation**: 
  - Backend: Pydantic models for request validation
  - Frontend: Form validation before submission
- **Authentication**: 
  - JWT-based authentication (future implementation)
  - Secure token storage and transmission
- **Data Protection**: 
  - No sensitive voter information stored
  - Sanitize all user inputs
  - Validate file uploads
- **Dependencies**: 
  - Regular security audits of dependencies
  - Automated vulnerability scanning

### Code Review Checklist
Before submitting code:
- [ ] Code follows project conventions and style guides
- [ ] Tests are written and passing
- [ ] Documentation is updated
- [ ] Error handling is comprehensive
- [ ] Performance considerations addressed
- [ ] Security implications reviewed
- [ ] No hardcoded secrets or credentials
- [ ] Accessibility considerations addressed (frontend)
- [ ] Browser compatibility tested (frontend)

### Development Workflow
1. **Start with documentation** (specs, designs)
2. **Write tests first** (if using TDD)
3. **Implement functionality**
4. **Verify through triple-gate process**:
   - Technical validation (code works correctly)
   - Human verification (manual testing confirms functionality)
   - Understanding validation (knowledge transfer complete)
5. **Update documentation**
6. **Submit for review**

## Technology-Specific Guidelines

### Python/FastAPI Specific Practices
- Use type hints consistently
- Follow PEP 8 style guide
- Use dependency injection for services
- Implement proper exception handling
- Use async/await for I/O-bound operations
- Structure API routes logically
- Use Pydantic for data validation
- Implement proper logging

### TypeScript/React Specific Practices
- Use functional components with hooks
- Implement proper TypeScript interfaces
- Use React.memo for performance optimization
- Follow component composition patterns
- Implement proper error boundaries
- Use custom hooks for reusable logic
- Follow accessibility best practices
- Use Tailwind utility classes consistently

### SQLAlchemy Specific Practices
- Use declarative models
- Implement proper relationships
- Use migrations for schema changes
- Optimize queries for performance
- Implement proper connection pooling
- Use transactions for data integrity
- Implement proper error handling

### Zustand Specific Practices
- Keep stores focused and minimal
- Use TypeScript for type safety
- Implement proper selectors
- Use middleware when needed
- Follow immutable update patterns
- Implement proper error handling
- Use devtools for debugging

## Task Definition Template

```markdown
# Task [NUMBER]: [TASK_NAME]

## Generated from Project Documentation

### Objective
[Clear, one-sentence description of what this task accomplishes]

### Context from Project Documentation
- **Related User Scenarios**: [Reference to specific scenarios]
- **Technical Requirements**: [From data model or technical specs]
- **Dependencies**: [What this task requires to be completed first]

### Technical Requirements
- [ ] [Specific technical requirement 1]
- [ ] [Specific technical requirement 2]
- [ ] [Integration requirement]
- [ ] [Quality/performance requirement]

### Acceptance Criteria
- [ ] [Measurable success criterion 1]
- [ ] [Measurable success criterion 2]
- [ ] [Integration success criterion]
- [ ] [Quality success criterion]

### Architecture Approach
**Recommended Next Step**: [Start with Task Architect / Go directly to Systematic Developer]

**Why**: [Brief explanation of complexity and approach needed]

### Implementation Scope
- **Files to Create/Modify**: [List of expected files]
- **Estimated Effort**: [Small (1-2 hours) / Medium (2-6 hours) / Large (6+ hours)]
- **Risk Level**: [Low / Medium / High]

### Success Definition
This task is complete when:
1. ✅ All technical requirements implemented
2. ✅ All acceptance criteria met
3. ✅ Triple-gate verification passed
4. ✅ Integration with existing code confirmed
5. ✅ Documentation updated

### Dependencies and Blockers
- **Depends On**: [Previous tasks that must be complete]
- **Blocks**: [Future tasks that depend on this]
- **External Dependencies**: [APIs, services, data sources needed]

### Context for Next Steps
When this task is complete, it enables:
- [Next logical development step]
- [Future features that become possible]
- [Integration opportunities]