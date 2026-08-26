# # Shared foundation — client, tools, dispatch, permissions

"""
agents/core.py: Core components for the AI agent sessions.

This module provides the shared foundation for all agent sessions (s01–s23).
It centralizes all core functionalities to ensure that no logic is duplicated
across session-specific files. Each session file imports from this module and
only contains the new mechanism being introduced in that session.

Exports:
    - client (Anthropic): The configured Anthropic API client.
    - MODEL (str): The ID of the language model to be used.
    - DEFAULT_SYSTEM (str): The default system prompt for the agent.
    - SNAPSHOTS (dict): An in-memory store for file content snapshots.
    - Synchronous Tools: run_bash, run_read, run_write, run_grep, run_glob, run_revert.
    - Asynchronous Tools: async_bash, async_read, async_write, async_grep, async_glob.
    - Tool Schemas: BASIC_TOOLS, EXTENDED_TOOLS for the Anthropic API.
    - Dispatch Maps: BASIC_DISPATCH, EXTENDED_DISPATCH, ASYNC_DISPATCH.
    - Governance: load_rules(), check_permission().
    - Agent Loops: stream_loop(), dispatch_tools().
"""

# Import standard library modules
import os  # Operating system interfaces
import re  # Regular expression operations
import asyncio  # Asynchronous I/O framework
import subprocess  # Subprocess management for shell commands
import glob as _glob  # Unix style pathname pattern expansion
from pathlib import Path  # Object-oriented filesystem paths
from typing import Dict, List, Tuple, Optional, Any  # Type hinting support

