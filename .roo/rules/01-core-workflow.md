# Core Systematic Development Workflow

## Universal Principles (All Projects, All Modes)

### Documentation-First Development
- **NEVER** start implementation without clear requirements
- **ALWAYS** have acceptance criteria before coding
- **ALWAYS** understand the problem before designing the solution

### Human-Controlled Verification  
- **AI can suggest** but humans decide
- **Human verification required** for all implementations
- **Understanding validation** ensures knowledge transfer

### Task Isolation
- **One task at a time** in active-task/ directory
- **Archive completed work** to preserve learning
- **Clear handoffs** between planning and implementation

## File Organization Rules
```
active-task/           # Current work only
├── task-definition.md # What we're building
├── progress.md        # Current status
└── [implementation files]

completed-tasks/       # Historical record
├── 001-[name]-DONE/   # Numbered for sequence
├── 002-[name]-DONE/   
└── 003-[name]-DONE/

docs/
├── planning/          # Project-wide documentation
└── templates/         # Reusable templates
```

## Mode Coordination Rules

### Task Coordinator → Architect → Systematic Developer
1. **Task Coordinator**: Project setup and task generation
2. **Task Architect**: Design and planning (no code)
3. **Systematic Developer**: Implementation with verification

### When to Use Each Mode
- **New features**: Always start with Task Architect
- **Bug fixes**: Usually go directly to Systematic Developer  
- **Refactoring**: Usually needs Task Architect first
- **Uncertainty**: Start with Task Coordinator

## Quality Gates (Universal)
Every implementation must pass:
1. **Gate 1** (AI Self-Check): Technical validation
2. **Gate 2** (Human Verification): Manual testing and review
3. **Gate 3** (Understanding): Knowledge validation

## Anti-Patterns to Avoid
❌ "Just write some code and see what happens"
❌ "AI generated it so it must be correct"
❌ "Tests pass so we're done"
❌ "We'll document it later"
❌ "This is too simple to need verification"