# Developer Guidelines Template

## Code Quality Standards

### General Principles
- **Readability**: Code should be self-documenting and clear
- **Consistency**: Follow established patterns within the project
- **Simplicity**: Prefer simple solutions over complex ones
- **Testability**: Write code that can be easily tested

### Error Handling
```[LANGUAGE]
// [Language-specific error handling examples will be inserted here]
// This template adapts based on your technology stack
```

### Testing Standards
- **Unit Tests**: Test individual functions and components
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user workflows
- **Minimum Coverage**: [Specify coverage requirements]

### Code Organization
```
[PROJECT_STRUCTURE]
src/
├── [component-directory]/    # [Description]
├── [utilities-directory]/    # [Description]  
├── [tests-directory]/        # [Description]
└── [config-directory]/       # [Description]
```

### Documentation Requirements
- **Function Documentation**: Document all public functions
- **API Documentation**: Document all endpoints/interfaces
- **README**: Keep project README current
- **Architecture Decisions**: Document significant choices

### Performance Guidelines
- **[Technology-Specific Performance Tips]**
- **Resource Management**: [Memory, connections, etc.]
- **Optimization Strategies**: [Caching, lazy loading, etc.]

### Security Practices
- **Input Validation**: Validate all user inputs
- **Authentication**: [Project-specific auth requirements]
- **Data Protection**: [Encryption, secure storage]
- **Dependencies**: Keep dependencies updated

### Code Review Checklist
Before submitting code:
- [ ] Code follows project conventions
- [ ] Tests are written and passing
- [ ] Documentation is updated
- [ ] Error handling is comprehensive
- [ ] Performance considerations addressed
- [ ] Security implications reviewed

### Development Workflow
1. **Start with documentation** (specs, designs)
2. **Write tests first** (if using TDD)
3. **Implement functionality**
4. **Verify through triple-gate process**
5. **Update documentation**
6. **Submit for review**

## Technology-Specific Guidelines
[This section will be customized based on your project's technology stack]

### [TECHNOLOGY_NAME] Specific Practices
- [Language/framework specific guidelines]
- [Common patterns and anti-patterns]
- [Tool recommendations]
- [Performance considerations]
```

### Task Definition Template (Auto-generated)

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