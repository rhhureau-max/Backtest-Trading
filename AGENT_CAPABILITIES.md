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

#### Memory Persistence Mechanism: The `store_memory` Tool

While agents don't have access to full discussion history, they can persist important information through the **`store_memory` tool**:

**What is `store_memory`?**
- Tool that allows agents to save factual information about the codebase
- Stored memories persist and can be retrieved in future agent sessions
- Saves facts about the code itself, NOT conversation history

**What can be stored:**
- ✅ Coding conventions and style preferences (e.g., "Use single quotes for strings")
- ✅ Important structural information (e.g., "Authentication uses JWT tokens")
- ✅ Build/test commands that have been verified (e.g., "Run tests with `npm test`")
- ✅ Best practices specific to the codebase (e.g., "Always sanitize user input with htmlEscape()")
- ✅ Architectural patterns (e.g., "Use repository pattern for data access")

**What CANNOT be stored:**
- ❌ Full conversation history or discussions
- ❌ Temporary context or task-specific information
- ❌ User preferences not related to the codebase
- ❌ Sensitive information or secrets

**Examples of good memories:**
- "Use Python typing hints for all function signatures"
- "Follow PEP 8 style guide for Python code"
- "Build the project with `npm run build && npm run test`"
- "Use Winston for logging throughout the application"
- "Database connections are managed through the ConnectionPool class"

**How it works:**
1. During a session, an agent identifies an important codebase convention or fact
2. The agent uses `store_memory` to save this information with proper context
3. In future sessions, agents can access these stored memories
4. This helps maintain consistency across different agent sessions

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

**Important Note about Personal/Custom Agents:**
Creating a personal agent does NOT enable saving or accessing previous discussion data. Personal agents:
- ❌ Cannot access previous conversation history
- ❌ Cannot save discussions between different invocations
- ❌ Do not have persistent memory of past interactions
- ✅ Start each session with a fresh context, just like the main agent
- ✅ Can only access what's in the repository (code, git history, documentation)

The same limitations apply to both custom agents and the main agent - neither can persist or access full discussion history.

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

### Frequently Asked Questions

**Q: Will creating a personal/custom agent allow me to save discussions with agents?**

**A: No.** Creating a personal or custom agent does not enable saving or accessing discussion history. Personal agents have the same limitations as the main agent:
- No access to previous conversation history
- No persistent memory of discussions
- Each invocation starts with a fresh context

The only way to preserve information across sessions is through:
- Code and documentation in the repository
- Git commits with descriptive messages
- The `store_memory` tool (for factual information about the codebase only)

**Q: How can I provide context to agents about previous work?**

**A:** Since agents can't access discussion history, provide context through:
1. **Detailed problem statements** - Include background and relevant information in issues/PRs
2. **Git commits** - Write descriptive commit messages that explain what and why
3. **Documentation** - Maintain up-to-date docs in the repository
4. **Code comments** - Document complex logic and decisions in the code itself
5. **Stored memories** - Use `store_memory` for codebase conventions and patterns

**Q: What is the `store_memory` tool and how does it work?**

**A:** As explained in the Memory Persistence Mechanism section above, `store_memory` allows agents to persist factual codebase information across sessions.

**What it stores:**
- Code conventions (e.g., "Always use TypeScript strict mode")
- Verified build/test commands (e.g., "Run tests with `pytest -v`")
- Architectural patterns (e.g., "Use MVC pattern for web routes")
- Styling rules (e.g., "Follow Airbnb JavaScript style guide")

**What it does NOT store:**
- Conversation history or discussions
- Temporary task information
- User personal preferences unrelated to code

**Example:** If an agent learns that your project uses "single quotes for all JavaScript strings" by examining the codebase, it can store this as a memory. Future agents can then access this memory and apply the same convention, ensuring consistency without having to re-analyze the entire codebase.

This helps maintain coding standards and conventions across different agent sessions.

### Summary
Agents operate independently in each session without access to previous discussion data. To maintain continuity across sessions, rely on:
- Git history and commits
- Stored memories (via `store_memory` tool)
- Documentation in the repository
- Clear problem statements and issue descriptions
