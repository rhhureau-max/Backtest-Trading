# Agent Capabilities and Discussion Data Access

## Question: Do agents have access to previous agent discussion data?

### Short Answer
**No**, agents do not have automatic access to previous agent discussion data from earlier sessions.

### Detailed Explanation

#### Session Context
- Each agent session starts with a **fresh context window**
- Agents do not retain memory between different invocations or sessions
- When a new agent session begins, it does not have access to:
  - Previous conversation history from earlier agent runs
  - Discussion data from other agents
  - Context from prior problem-solving attempts

#### What Agents CAN Access
Agents have access to:
1. **Repository Code**: The current state of the code in the repository
2. **Git History**: Commit messages, diffs, and historical changes
3. **Current PR/Issue Context**: The problem statement provided for the current session
4. **Documentation**: Any documentation files in the repository
5. **Stored Memories**: Facts explicitly stored using the `store_memory` tool during previous sessions

#### Memory Persistence Mechanism
While agents don't have access to full discussion history, they can persist important information through the **`store_memory` tool**:

- **Purpose**: Store important facts, conventions, or context about the codebase
- **Persistence**: These memories are saved and can be retrieved in future sessions
- **Scope**: Limited to factual information about the codebase, not full conversation history
- **Usage**: Agents can store:
  - Coding conventions and preferences
  - Important structural information
  - Build/test commands that have been verified
  - Best practices specific to the codebase

#### Example Use Cases

**Scenario 1: Continuing Previous Work**
If a previous agent worked on feature X and you need to continue that work:
- ❌ You won't have access to the previous agent's thought process or discussion
- ✅ You can review the git commits to see what changes were made
- ✅ You can read any stored memories about conventions or patterns

**Scenario 2: Learning from Past Mistakes**
If a previous agent made changes that needed to be reverted:
- ❌ You won't know why those changes were attempted
- ✅ You can see the git history showing what was changed and reverted
- ✅ If a memory was stored about a lesson learned, you can access that

#### Custom Agents
Custom agents are specialized agents with their own separate context:
- Each custom agent has its own **private context window**
- Custom agents do NOT share context with the main agent
- When invoking a custom agent, you must pass all necessary context explicitly
- Each invocation of a custom agent starts fresh

#### Best Practices for Context Continuity

1. **Use Git Effectively**
   - Write descriptive commit messages
   - Reference issue numbers in commits
   - Document major decisions in commit messages

2. **Store Important Memories**
   - Use `store_memory` for codebase conventions
   - Store verified build/test commands
   - Record architectural decisions

3. **Maintain Documentation**
   - Keep README and other docs updated
   - Document complex logic in code comments
   - Create ADR (Architecture Decision Records) for major decisions

4. **Explicit Context in Issues/PRs**
   - Provide comprehensive problem statements
   - Link to related issues and PRs
   - Include relevant background information

### Summary
Agents operate independently in each session without access to previous discussion data. To maintain continuity across sessions, rely on:
- Git history and commits
- Stored memories (via `store_memory` tool)
- Documentation in the repository
- Clear problem statements and issue descriptions
