# Project Kickoff and Task Generation Protocol

## Kickoff Triggers
Respond to these phrases with kickoff protocol:
- "start systematic development"
- "documentation complete, what's next?"
- "ready to begin development"
- "how do we start the structured process?"

## Kickoff Process

### Step 1: Project Type Detection
Ask these questions to understand the project:

**Essential Questions:**
1. "What type of project is this?" (web app, API, library, CLI tool, etc.)
2. "What's your primary technology stack?" (TypeScript, Python, Go, etc.)
3. "What's the expected scale?" (prototype, production, high-scale)

### Step 2: Documentation Recommendations
Based on answers, recommend appropriate documentation set:

**Example Response:**
"For a [PROJECT_TYPE] using [TECHNOLOGY], I recommend these documents:

**Core (Required)**:
- project-purpose.md
- acceptance-criteria.md  
- developer-guidelines.md

**Project-Specific (Choose 2-3)**:
- [specific docs based on project type]

Would you like me to generate templates for these documents?"

### Step 3: Template Generation
Create appropriate templates in docs/planning/ directory using templates from docs/templates/

### Step 4: Development Roadmap
Once documentation exists, analyze and create development sequence:

```
📋 **DEVELOPMENT ROADMAP**

Based on your documentation, here's the recommended build sequence:

**Foundation Tasks** (Build First):
1. [Foundation task 1]
2. [Foundation task 2]

**Feature Tasks** (Build Second):  
3. [Feature task 1]
4. [Feature task 2]

**Integration Tasks** (Build Last):
5. [Integration task 1]

Recommended starting point: **[First specific task]**

Ready to start? Type "start task 1" to begin.
```

### Step 5: First Task Setup
When developer confirms, automatically:
- Create active-task/ directory structure
- Generate task-definition.md from project docs
- Initialize progress.md
- Recommend next mode (usually Task Architect)

## Task Generation Rules
First task should be:
- ✅ Foundational (other tasks depend on it)
- ✅ Clearly scoped (2-4 hours of work)
- ✅ Low risk (hard to mess up)
- ✅ Immediately actionable

## Common First Tasks by Project Type
- **Web App**: Core data models and types
- **API Service**: Basic schemas and validation
- **Library**: Core interfaces and basic structure
- **CLI Tool**: Argument parsing and basic commands