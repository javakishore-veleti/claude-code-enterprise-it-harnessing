# claude-code-from-scratch

## What is Harness Engineering?
Harness engineering is the discipline of building the environment that surrounds an AI model, not the model itself. The model reasons and decides. The harness executes, constrains, and connects. A well-designed harness gives the model precisely the tools it needs, nothing more, and governs exactly what it is allowed to do with them.

If we break down the concept of harness engineering into four core principles, they would be:

- The model is the only source of decisions, the harness never branches on model output, it only executes what the model requests
- Tools are the only interface between the model and the world, every action, from reading a file to spawning a subagent, goes through a typed, schema-validated tool call
- Context is a managed resource, what the model sees at each turn is curated, compressed, and injected deliberately, not accumulated blindly
- Permissions are declarative, not procedural, what is allowed, what is blocked, and what requires approval is defined in configuration, not scattered across conditional logic

## How Claude Code Uses Harness Engineering?
Claude Code is not an agent framework. It is a harness, one of the most carefully engineered ones ever deployed in production. Anthropic did not build logic to decide when to read files or when to run tests. They gave Claude the tools to do those things and trusted the model to decide when they were needed.

Claude Code architecture follows the principles of harness engineering in several ways:

1. The master loop is stateless and generic, it runs identically whether the task is a one-line fix or a multi-hour refactor, because all task-specific intelligence lives in the model

2. The tool registry is the only extension point, adding a new capability to Claude Code means registering one new tool, with a name, a description, and an input schema

3. Context is actively managed at ~92% window usage, older conversation turns are summarised and persisted to disk, keeping the model’s working memory focused on the current task

4. Permission governance runs as a pre-execution layer, every tool call passes through a rule evaluation before the harness executes it, making safety a structural property rather than a model behavior.

5. System prompt is the foundation of the agent’s behavior, system prompt is not useful most often but it is critical to set the stage for how the model will approach tasks.

### Phase 1: The Core Agent Loop
The agent loop is the single architectural primitive that everything else builds on. Before tools, before permissions, before multi-agent coordination, there is a loop that calls the model, observes what it wants to do, executes it, and feeds the result back.

#### Minimal While Loop:
The most fundamental principle of any agentic system is the perception-action-observation cycle.

- The agent receives a task, attempts a solution using a tool
- Observes the result, and decides whether to continue or stop all driven by the model, not the code.

This is not a retry loop or a fallback mechanism. It is the core reasoning engine. In Claude Code, this is the nO master loop, the same loop that runs whether you ask Claude to fix a one-line bug or refactor an entire codebase. The code never changes. Only what the model decides to do inside it changes.

To build the most basic phenomenon of Claude code using anthropic model we first have to initialize the client along with the model.

The claude is build around tools, so we need to define some basic tools for our agent to interact with the world. These tools will be the interface through which the model can perform actions and gather information.

The tool definitions are equally important. These are what the model reads to decide which tool to call — and the description field is not documentation, it is an instruction.

A poorly written description causes the model to pick the wrong tool. If grep says "search files" and bash says "run commands", the model will use bash for every search operation because the description does not constrain it precisely enough.

Claude Code's internal tool descriptions are extremely specific about when each tool should be used this specificity is what produces consistent, predictable tool selection across millions of executions.

The handler functions themselves follow a consistent contract — they accept a dict of inputs, return a string, and never raise exceptions to the loop. Errors are returned as strings, not thrown.

#### TodoWrite Planning Before Execution
One of the most revealing findings from reverse-engineered Claude Code execution traces is what Claude does before it writes a single line of code or reads a single file on a complex task. It calls TodoWrite. Every time.

The plan comes before the action, and the action is only taken once the plan is committed.

1. This is not accidental. Anthropic observed that without an explicit planning mechanism, the model drifts on multi-step tasks.
2. It starts executing, encounters an intermediate result that looks interesting, follows it, and surfaces twenty minutes later having done something adjacent to but not exactly what was asked.
3. The TodoWrite tool solves this at the architectural level — not by making the model smarter, but by giving it a commitment mechanism that it holds itself accountable to throughout execution.

Claude Code injects the current todo state as a system reminder after every tool call. The model cannot forget what it planned to do because the plan is continuously re-injected into its context. This is what allows Claude Code to reliably complete tasks that span dozens of tool calls without losing track of the goal.

Three tools work together as a unit. todo_write commits the full plan at the start. todo_update marks each step as the agent moves through it. todo_read lets the model check its own progress at any point.

Together they create an external working memory that keeps the execution honest — the model cannot silently skip steps because each step has a status that persists across turns.

The system prompt is updated to make planning mandatory.

#### Subagent Context Isolation
Claude Code’s execution traces reveal something interesting about how it handles large codebase exploration.

1. When asked to understand a new repository, Claude does not read files directly into the main conversation.
2. It spawns three parallel explore subagents, each with a different focus, each running in complete isolation from the main context. The main conversation receives three clean summaries.
3. It never sees the dozens of intermediate file reads, grep outputs, and directory listings that produced them.

This is subagent context isolation, the pattern that allows Claude Code to work on arbitrarily large codebases without the main conversation window filling with noise. Every intermediate result that is irrelevant to the final answer stays inside the subagent and is discarded when it finishes. The parent only pays for the context it actually needs.

The isolation is implemented by giving each subagent a completely independent messages[] list. There is no shared state between parent and child except the final text response that the child returns.

The subagent runs the exact same agent loop as the parent. It has access to the exact same tools. The only difference is its messages[] list starts empty and its system prompt focuses it on a bounded task. When it finishes, everything it accumulated, every file read, every grep output, every intermediate reasoning step is discarded. Only the final summary crosses back into the parent.

This is registered as a tool so the model can decide when to use it.

The isolation is what keeps the main agent’s reasoning at the right level of abstraction.

### Phase 2: Knowledge & Context Management
The third phase is about the cognitive infrastructure where the agent moves beyond single-session execution loading domain knowledge only when it is needed.

Compressing conversation history before it degrades reasoning quality, and persisting task state to disk so that work survives process restarts. This is where Claude Code’s skill system, compressor wU2, and long-term memory file come from.

#### On-Demand Skill Loading
One of the most expensive mistakes in harness engineering is putting everything the model might need into the system prompt.

A system prompt that contains PDF processing guides, code review methodologies, deployment checklists, and security auditing frameworks would consume thousands of tokens on every single API call the vast majority of it irrelevant to whatever the model is currently doing.
Claude Code solves this with progressive disclosure, the same pattern that makes its skill system one of its most architecturally clean components.

The model system prompt contains only one-line descriptions of available skills. When the model recognises it needs domain expertise for the current task, it calls load_skill() and the full instructions are injected via a tool result directly into the conversation at the exact moment they are needed. The model pays the context cost only when the knowledge is actually relevant. Install a hundred skills and the system prompt grows by a hundred lines, not a hundred pages.

The skill files themselves follow a consistent format — a metadata header for discovery, and a full body of procedural instructions that the model reads and applies.

The discovery mechanism scans the skills directory at startup, reads only the metadata header from each SKILL.md, and builds a lightweight registry that goes into the system prompt.

The system prompt references all available skills without loading any of them.

Without the skill, the model would have reviewed code but inconsistently, without enforced categorisation, and without the deploy-readiness summary. The skill does not make the model smarter. It makes the model’s output consistent and structured across every code review it will ever perform.

#### Three-Layer Context Compression
Every long-running session hits the same wall. The context window fills with tool outputs, intermediate results, and conversation turns that were relevant ten minutes ago but are now just noise.

Claude Code’s compressor wU2 triggers automatically at approximately 92% context window usage.

It does not discard history, it summarises it, keeping the information while dramatically reducing the token footprint. The summary is then written to a persistent markdown file on disk, making the agent's memory durable across session restarts.

The implementation uses three explicit layers that process history in order. Recent messages are kept verbatim because they contain the active reasoning context. Older messages are collapsed into a single summary block via a dedicated compression API call. That summary is written to .agent_memory.md so the next session can load it and continue without starting from scratch.

The compression function is called after every agent response turn not on a timer, but based on measured context size.

At session startup, the agent checks for an existing memory file and loads it before the first user message.

After a long session of reading, writing, and testing, compression triggered automatically. The 18 accumulated messages — file contents, test outputs, intermediate reasoning — collapsed into one summary block. The next time this session starts, it loads that summary and continues with full context about what was accomplished, without paying for 18 turns of history on every subsequent API call.

#### File-Based Task Dependency Graph
Context compression keeps the conversation window manageable. But it solves a different problem from task tracking. Compression is about what the model remembers.

The task graph is about what the agent commits to doing across sessions, across restarts, and eventually across multiple agents working in parallel.

Claude Code TodoWrite system is session-scoped. Close the terminal and the plan is gone. The task graph in this session extends that into a persistent, dependency-aware structure. Each task carries an ID, a description, a status, a priority level, and an explicit list of upstream task IDs that must be completed before it becomes available.

The graph lives in .agent_tasks.json and survives everything, process crashes, session restarts, and machine reboots.

This is the foundation that Phase 4 multi-agent system builds on. When multiple agents run in parallel, they all read from and write to the same task graph. The dependency system ensures they never execute a task before its prerequisites are complete, and the atomic claiming mechanism in Phase 4 ensures no two agents claim the same task simultaneously.

The threading lock on every read-write operation is critical. In Phase 4, multiple agents will call _load() and _save() concurrently.

Without the lock, two agents can read the same state simultaneously, each modify it independently, and the second write silently overwrites the first agent's changes. The lock makes every task state transition atomic.

The agent created the full task graph first, identified the dependency chain automatically, and then executed tasks in the correct order never attempting a task before its upstream dependency was marked complete.

The graph persisted to disk throughout, meaning if the process had crashed after task 3, a restart would have found tasks 1–3 done and continued from task 4 without repeating any work.

This is the behaviour that makes the task graph a fundamentally different mechanism from TodoWrite not just planning for one session, but a durable project state that survives anything.

### Phase 3: Async Execution & Multi-Agent Teams
The fourth phase is about breaking the single-agent ceiling where one context window and one execution thread are no longer enough running slow operations in background threads without blocking the main loop, delegating parallel workstreams to persistent specialist agents, governing inter-agent communication with a finite state machine, enabling autonomous task claiming without a central coordinator, and isolating parallel file writes at the git worktree level.

This is where Claude Code’s parallel subagent spawning, background execution queue, and task delegation architecture are reconstructed from first principles.

#### Background Task Execution with Notifications
In Claude Code’s internal architecture, the h2A async queue is one of its most practical performance mechanisms. When Claude runs a test suite, compiles a project, or performs a long database migration, it does not sit idle waiting for the result.

It pushes the operation into the background, continues planning the next steps, and receives a notification when the operation completes. The main reasoning loop never blocks on I/O.