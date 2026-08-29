#!/usr/bin/env python3
"""
s07_task_system.py: Implementation of a Persistent, Dependency-Aware Task Graph.

Motto: "Break big goals into small tasks, order them, persist to disk"

This module evolves the planning capability of the agent by moving from a 
simple list (s03) to a robust, file-based task management system. It allows 
the agent to handle complex projects by defining tasks that depend on the 
completion of others.

Key Architectural Concepts:
    1. Directed Acyclic Graph (DAG): Tasks can depend on one or more previous 
       tasks, creating a logical order of operations.
    2. Unique Identification: Every task is assigned a short, unique UUID 
       to prevent ambiguity during updates.
    3. State Persistence: The entire graph is serialized to `.agent_tasks.json`, 
       enabling the agent to resume work across restarts or hand work 
       off to other agents (s09+).
    4. Dependency Resolution: The `task_next` tool provides automated 
       logic to identify the next actionable item that isn't blocked.
    5. Project Namespacing: Tasks carry an agent-assigned `project` tag so 
       that unrelated efforts (e.g. a Spring Boot app vs. a Django app) 
       don't create noise in `task_list`/`task_next`. The USER never types 
       this — the agent infers a short slug from context and fills it in 
       automatically, the same way it already infers `priority` silently.
       As a safety net for anything left untagged (or tagged "default"), 
       `task_list` also auto-groups tasks by connected component of the 
       `depends_on` graph, so chains that are properly linked still cluster 
       correctly even with zero explicit tagging.

Task Schema:
    - ID: 8-character unique hex string.
    - Status: [pending, in_progress, done, failed].
    - Dependencies: List of IDs that must be 'done' before this task starts.
    - Project: Agent-assigned slug grouping tasks belonging to the same effort.
"""
# === Standard Library Imports ===
import os      # Operating system interfaces
import json    # JSON serialization for task persistence
import uuid    # Unique identifier generation
import sys     # System-specific parameters and functions
from pathlib import Path  # Object-oriented filesystem paths
from typing import List, Dict, Any, Union, Optional, Set  # For strict type hinting

# === Local Module Imports ===
from core import (
    EXTENDED_TOOLS,      # Base tools (bash, read, write, etc.)
    EXTENDED_DISPATCH,   # Mapping for base tools
    stream_loop          # The core autonomous loop logic
)

# === Configuration and Constants ===

# File where the task graph is persisted.
TASKS_FILE: Path = Path(".agent_tasks.json")

# Default project label used when the agent doesn't provide one explicitly.
# Tasks left at this default are still grouped sensibly via connected
# components in run_task_list() as a fallback.
DEFAULT_PROJECT: str = "default"

# Specialized System Prompt: Instructs the agent on task management protocol.
SYSTEM: str = (
    f"You are a coding agent at {os.getcwd()}. "
    "Use the task system to manage complex work: create tasks, respect dependencies, "
    "and mark progress. Always call task_list or task_next before starting work "
    "to ensure you are working on the correct unblocked priority. "
    "When starting a new, distinct effort (e.g. a different app/feature/tech stack "
    "than what's already in the task graph), silently choose a short project slug "
    "(e.g. 'spring-boot-webapp', 'django-webapp') and pass it as the 'project' "
    "argument on every task_create call for that effort. Never ask the user for a "
    "project name — infer it yourself from context. When filtering task_list or "
    "task_next, pass 'project' only if the user is clearly focused on one effort."
)

# === Task Graph I/O Helpers ===

def _load_tasks() -> List[Dict[str, Any]]:
    """
    Reads the task graph from the local JSON file.

    Returns:
        List[Dict[str, Any]]: The list of task objects. Returns empty list if 
                              file is missing or corrupt.
    """
    if not TASKS_FILE.exists():
        return []
    try:
        # Load and parse the JSON task list
        return json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, IOError):
        # Fallback for corrupted files
        return []


def _save_tasks(tasks: List[Dict[str, Any]]) -> None:
    """
    Serializes the current task graph to the local JSON file.

    Args:
        tasks (List[Dict[str, Any]]): The list of tasks to persist.
    """
    try:
        # Write with indentation for human-readability (debugging)
        TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
    except IOError as e:
        print(f"\033[31m[error] Failed to save tasks: {e}\033[0m")


def _connected_components(tasks: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Groups tasks into connected components using their `depends_on` edges
    (treated as undirected for clustering purposes). This is a zero-config,
    zero-user-input fallback grouping: any chain of properly-linked tasks
    clusters together automatically, even if nobody set a `project` tag.

    Args:
        tasks (List[Dict[str, Any]]): The full task list.

    Returns:
        Dict[str, List[Dict[str, Any]]]: Mapping of a representative root ID
                                          to the list of tasks in that component.
    """
    parent: Dict[str, str] = {t["id"]: t["id"] for t in tasks}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    ids = {t["id"] for t in tasks}
    for t in tasks:
        for dep in t.get("depends_on", []):
            if dep in ids:
                union(t["id"], dep)

    groups: Dict[str, List[Dict[str, Any]]] = {}
    for t in tasks:
        root = find(t["id"])
        groups.setdefault(root, []).append(t)
    return groups

# === Tool Implementations ===

def run_task_create(
    description: str,
    depends_on: Optional[List[str]] = None,
    priority: str = "medium",
    project: str = DEFAULT_PROJECT,
) -> str:
    """
    Creates a new task and adds it to the persistent graph.

    Args:
        description (str): Text describing the work to be done.
        depends_on (List[str], optional): List of IDs this task depends on.
        priority (str): Level of importance [high, medium, low].
        project (str): Agent-assigned slug grouping this task with related
                        tasks from the same effort. Defaults to "default" so
                        single-project use is unaffected. This is filled in
                        by the AGENT, never by prompting the user directly.

    Returns:
        str: Success message including the generated task ID.
    """
    tasks = _load_tasks()
    
    # Generate a unique 8-character ID for the task
    task_id = uuid.uuid4().hex[:8]
    
    new_task = {
        "id":          task_id,
        "description": description,
        "status":      "pending",
        "priority":    priority,
        "depends_on":  depends_on or [],
        "project":     project or DEFAULT_PROJECT,
        "result":      "", # To be filled upon completion
    }
    
    tasks.append(new_task)
    _save_tasks(tasks)
    
    return f"Created task {task_id} [project={new_task['project']}]: {description}"

def run_task_list(project: Optional[str] = None) -> str:
    """
    Generates a formatted summary of tasks in the system, grouped by project.

    Args:
        project (str, optional): If given, only show tasks whose `project`
                                  field matches (case-insensitive). If omitted,
                                  show everything, grouped.

    Returns:
        str: A table-like string showing status, priority, deps, and description,
             sectioned by project so unrelated efforts don't blur together.
    """
    tasks = _load_tasks()
    if not tasks:
        return "(no tasks currently in the system)"

    if project:
        tasks = [t for t in tasks if t.get("project", DEFAULT_PROJECT).lower() == project.lower()]
        if not tasks:
            return f"(no tasks found for project '{project}')"

    def fmt(t: Dict[str, Any]) -> str:
        deps_str = f" [needs: {','.join(t['depends_on'])}]" if t.get("depends_on") else ""
        return f"  [{t['id']}] [{t['status']:12s}] [{t['priority']:6s}]{deps_str} {t['description']}"

    # Group by explicit project tag first.
    by_project: Dict[str, List[Dict[str, Any]]] = {}
    for t in tasks:
        by_project.setdefault(t.get("project", DEFAULT_PROJECT), []).append(t)

    lines: List[str] = []
    for proj_name in sorted(by_project.keys()):
        proj_tasks = by_project[proj_name]
        lines.append(f"=== project: {proj_name} ({len(proj_tasks)} tasks) ===")

        # Within an untagged/default bucket, fall back to connected components
        # so properly-linked chains still visually separate from unrelated
        # orphan tasks that just happen to share the default label.
        if proj_name == DEFAULT_PROJECT and len(proj_tasks) > 1:
            components = _connected_components(proj_tasks)
            for i, (_, members) in enumerate(components.items(), 1):
                if len(components) > 1:
                    lines.append(f"  -- component {i} --")
                for t in members:
                    lines.append(fmt(t))
        else:
            for t in proj_tasks:
                lines.append(fmt(t))

    return "\n".join(lines)

def run_task_update(task_id: str, status: str, result: str = "") -> str:
    """
    Updates the status or recorded result of an existing task.

    Args:
        task_id (str): The unique ID (or prefix) of the task to update.
        status (str): The new status [pending, in_progress, done, failed].
        result (str, optional): A summary of the work performed.

    Returns:
        str: Success or error message.
    """
    tasks = _load_tasks()
    found = False
    
    for t in tasks:
        # Support updating by full ID or a unique prefix
        if t["id"].startswith(task_id):
            t["status"] = status
            if result:
                t["result"] = result
            found = True
            actual_id = t["id"]
            break
            
    if found:
        _save_tasks(tasks)
        return f"Task {actual_id} successfully updated to '{status}'"
    
    return f"Error: Task with ID '{task_id}' not found."

def run_task_next(project: Optional[str] = None) -> str:
    """
    Algorithm to find the next actionable task based on dependencies.

    This identifies 'pending' tasks where all prerequisite tasks are 'done'.

    Args:
        project (str, optional): If given, only consider tasks tagged with
                                  this project, so suggestions from an
                                  unrelated effort don't surface as noise.

    Returns:
        str: The description of the next task or a status message.
    """
    tasks = _load_tasks()

    if project:
        scoped = [t for t in tasks if t.get("project", DEFAULT_PROJECT).lower() == project.lower()]
    else:
        scoped = tasks

    # Dependency completion is checked against the FULL graph (done_ids),
    # not just the scoped subset, in case a task legitimately depends on
    # something tagged under a different project label.
    done_ids: Set[str] = {t["id"] for t in tasks if t["status"] == "done"}
    
    for t in scoped:
        # We only care about tasks that haven't started yet
        if t["status"] != "pending":
            continue
            
        # Check if every dependency for this task is in the 'done_ids' set
        dependencies = t.get("depends_on", [])
        if all(dep in done_ids for dep in dependencies):
            proj_tag = t.get("project", DEFAULT_PROJECT)
            return f"Suggested Next Task: [{t['id']}] (Priority: {t['priority']}, Project: {proj_tag}) - {t['description']}"

    if project:
        return f"No unblocked tasks available for project '{project}'. Either it's fully done or blocked by a dependency circularity."
    return "No unblocked tasks available. Either all tasks are done or there is a dependency circularity."

# === Tool Schema and Dispatch Extensions ===

# Define the task-related tools for the Anthropic API
TASK_TOOLS: List[Dict[str, Any]] = EXTENDED_TOOLS + [
    {
        "name": "task_create",
        "description": (
            "Create a new task in the persistent dependency graph. "
            "Always pass 'project' with a short slug you infer from context "
            "(e.g. 'spring-boot-webapp') when starting a new, distinct effort, "
            "so it doesn't blend with unrelated tasks. Never ask the user for this."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "description": {"type": "string", "description": "What needs to be done."},
                "depends_on":  {
                    "type": "array", 
                    "items": {"type": "string"},
                    "description": "List of task IDs this task depends on."
                },
                "priority":    {"type": "string", "enum": ["high", "medium", "low"]},
                "project":     {
                    "type": "string",
                    "description": (
                        "Short agent-inferred slug grouping this task with related "
                        "tasks from the same effort (e.g. 'spring-boot-webapp', "
                        "'django-webapp'). Defaults to 'default' if omitted."
                    ),
                },
            },
            "required": ["description"],
        },
    },
    {
        "name": "task_list",
        "description": (
            "Show tasks, their IDs, status, and dependency requirements, "
            "grouped by project so unrelated efforts don't create noise. "
            "Optionally filter to a single project."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "project": {
                    "type": "string",
                    "description": "If set, only show tasks tagged with this project.",
                },
            },
        },
    },
    {
        "name": "task_update",
        "description": "Change the status of a task or record its final result.",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "8-char ID of the task."},
                "status":  {"type": "string", "enum": ["pending", "in_progress", "done", "failed"]},
                "result":  {"type": "string", "description": "Brief summary of work done."},
            },
            "required": ["task_id", "status"],
        },
    },
    {
        "name": "task_next",
        "description": (
            "Consult the graph logic to find the next task that is not blocked "
            "by dependencies. Optionally scope to a single project so suggestions "
            "from an unrelated effort don't surface."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "project": {
                    "type": "string",
                    "description": "If set, only consider tasks tagged with this project.",
                },
            },
        },
    },
]

# Map the task tools to their Python implementations
TASK_DISPATCH: Dict[str, Any] = {
    **EXTENDED_DISPATCH, # Inherit base tools
    "task_create": lambda inp: run_task_create(
        inp["description"], 
        inp.get("depends_on"), 
        inp.get("priority", "medium"),
        inp.get("project", DEFAULT_PROJECT),
    ),
    "task_list":   lambda inp: run_task_list(inp.get("project")),
    "task_update": lambda inp: run_task_update(
        inp["task_id"], 
        inp["status"], 
        inp.get("result", "")
    ),
    "task_next":   lambda inp: run_task_next(inp.get("project")),
}


# === Main Execution Block ===

def main() -> None:
    """
    Initializes the terminal interaction for the s07 'Task System' agent.
    """
    # UI Header in Gray
    print(f"\033[90ms07: file-based task graph | tasks → {TASKS_FILE}\033[0m\n")
    
    # Interaction history for the current session
    history: List[Dict[str, Any]] = []

    # Main Command Loop (REPL)
    while True:
        try:
            # User Prompt in Cyan
            query: str = input("\033[36ms07 >> \033[0m").strip()
        except (EOFError, KeyboardInterrupt):
            # Graceful exit handlers
            print("\nExiting session.")
            sys.exit(0)

        # Standard exit check
        if not query or query.lower() in ("q", "exit", "quit"):
            break

        # Record query
        history.append({"role": "user", "content": query})
        
        # Start the autonomous loop with the new task tools and system prompt
        stream_loop(
            messages=history,
            tools=TASK_TOOLS,
            dispatch=TASK_DISPATCH,
            system=SYSTEM
        )
        
        # Visual spacer
        print()


if __name__ == "__main__":
    # Script entry point
    main()
