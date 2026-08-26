#!/usr/bin/env python3

"""
s01_perception_action_loop.py: The Fundamental AI Agent Interaction Loop. 

The minimal while loop — core agent pattern. 

Motto: "One loop & bash is all you need"

This script serves as the entry point for the agent series, demonstrating the  foundational "Thinking-Acting" cycle. It implements a synchronous interaction 
pattern where the LLM is prompted, evaluates if it needs to use a tool (specifically  the 'bash' tool in this session), executes that tool, and continues 
until a final text response is produced.

The loop handles:
    1. Message history state management.
    2. API communication with Anthropic.
    3. Conditional logic based on 'stop_reason'.
    4. Synchronous tool dispatching.

"""
