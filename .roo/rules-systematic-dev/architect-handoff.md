# Architect → Systematic Developer Handoff Protocol

## Required Architecture Deliverables
Before Systematic Developer can begin implementation, Task Architect must provide:

### Required Files in active-task/:
- [ ] **task-architecture.md** - Complete system design
- [ ] **implementation-plan.md** - Step-by-step approach  
- [ ] **interfaces.md** - All contracts and APIs defined
- [ ] **file-structure.md** - Code organization plan

### Architecture Completeness Check
Systematic Developer must verify before any coding:

```
🏗️ **ARCHITECTURE VALIDATION**

Checking for required architecture documentation...

✅ task-architecture.md - System design complete
✅ implementation-plan.md - Implementation steps defined  
✅ interfaces.md - All contracts specified
✅ file-structure.md - Code organization planned

Architecture documentation complete. Ready for implementation.
```

### If Architecture Missing:
```
🚨 **ARCHITECTURE INCOMPLETE**

Required architecture documentation missing:
- [ ] task-architecture.md
- [ ] implementation-plan.md  
- [ ] interfaces.md

Cannot proceed with systematic implementation. Please:
1. Switch to Task Architect mode: /architect
2. Complete the architecture documentation
3. Return to Systematic Developer mode when planning is done
```

## Handoff Quality Standards

### Task Architect Must Provide:
- **Clear requirements** - No ambiguous specifications
- **Defined interfaces** - All APIs and contracts specified
- **Implementation approach** - Step-by-step plan
- **File organization** - Where code should be placed
- **Key decisions explained** - Rationale for architectural choices

### Systematic Developer Must Verify:
- **Architecture makes sense** for the requirements
- **Implementation plan is actionable** and clear
- **All interfaces are fully specified**
- **Approach aligns with project guidelines**

## Handoff Message Template
When Task Architect completes planning:

```
🎯 **ARCHITECTURE → IMPLEMENTATION HANDOFF**

Architecture phase complete for: [TASK NAME]

**Deliverables Ready**:
✅ System architecture designed
✅ Implementation plan created
✅ All interfaces defined  
✅ File structure planned

**Ready for Implementation**:
Switch to Systematic Developer mode and begin triple-gate implementation.

Architecture decisions documented in active-task/ directory.
```

## Implementation Guidance
Systematic Developer should:
- **Follow the architecture** exactly as designed
- **Implement step-by-step** according to the plan
- **Use defined interfaces** without modification
- **Apply triple-gate verification** to ensure quality
- **Ask for clarification** if architecture is unclear (return to Architect)

This ensures clean separation between thinking (Architect) and building (Systematic Developer).