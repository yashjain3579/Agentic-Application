"""
Agentic Application - Tool-based autonomous agent system.

This module provides a production-grade agentic system where an AI-like agent
autonomously decides which tools to use, in what sequence, and loops until
a task is complete. It handles complex queries with multiple steps, error handling,
and comprehensive validation.
"""

from .app import AgenticApp, create_app
from .agent import Agent
from .tools import ToolRegistry, Tool, ToolType, ToolParameter

__version__ = "1.0.0"
__author__ = "Agentic App Team"

__all__ = [
    "AgenticApp",
    "create_app",
    "Agent",
    "ToolRegistry",
    "Tool",
    "ToolType",
    "ToolParameter",
]
