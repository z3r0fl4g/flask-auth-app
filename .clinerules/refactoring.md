# Codebase Refactoring Rules

## General Principles

1. **Incremental Changes**:

   - Refactor in small, focused steps
   - Each change should be independently testable
   - Maintain working state throughout

2. **Documentation**:

   - Update docstrings before refactoring
   - Document architectural decisions
   - Maintain changelog of refactors

3. **Testing**:
   - 100% test coverage for refactored code
   - Tests must pass before and after
   - Add new tests for changed behavior

## Specific Guidelines

### Authentication Refactoring

1. **Route Organization**:

   - Group related routes by functionality
   - Separate concerns (auth, profile, admin)
   - Use consistent naming patterns

2. **Security Refactors**:

   - Isolate security-sensitive code
   - Document security implications
   - Review with security checklist

3. **Database Refactors**:
   - Use Alembic for schema changes
   - Maintain backwards compatibility
   - Test migrations thoroughly

### Code Quality

1. **Function Length**:

   - Max 50 lines per function
   - Split larger functions
   - Single responsibility principle

2. **Class Design**:

   - Cohesive responsibilities
   - Proper encapsulation
   - Clear interfaces

3. **Error Handling**:
   - Consistent error responses
   - Meaningful error messages
   - Proper logging

## Refactoring Process

1. **Pre-Refactor Steps**:

   - Create backup branch
   - Document current behavior
   - Write characterization tests

2. **During Refactor**:

   - Commit after each successful step
   - Verify tests continuously
   - Check performance impact

3. **Post-Refactor**:
   - Update documentation
   - Review with team
   - Monitor production impact

## Approval Process

- Major refactors require:
  - Design review
  - Security review
  - Performance assessment
  - Team sign-off
