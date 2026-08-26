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

# === Optional Dependencies for Enhanced User Experience ===

# Attempt to configure 'readline' for better CLI input handling on Unix-based systems
try:
    import readline  # Provides line editing and history features
    # Disable special character binding that can interfere with terminal output
    readline.parse_and_bind("set bind-tty-special-chars off")
    # Enable handling of 8-bit input characters
    readline.parse_and_bind("set input-meta on")
    # Enable output of 8-bit characters
    readline.parse_and_bind("set output-meta on")
    # Prevent conversion of 8-bit characters to ASCII sequences
    readline.parse_and_bind("set convert-meta off")
except ImportError:
    # Fail silently if readline is unavailable (e.g., on standard Windows installations)
    pass

# Attempt to initialize 'colorama' for cross-platform colored terminal support
try:
    from colorama import init as _colorama_init  # Import the initialization function
    _colorama_init()  # Execute initialization to wrap stdout/stderr
except ImportError:
    # Fail silently if colorama is not installed in the environment
    pass


# Import third-party libraries
import yaml  # YAML parser and emitter for configuration files
from anthropic import Anthropic  # Official Anthropic API Python SDK
from dotenv import load_dotenv  # Loads variables from .env into environment
