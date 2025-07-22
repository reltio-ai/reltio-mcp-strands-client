"""
Reltio MCP Strands Client.

A minimalistic client for connecting Strands AI agents to Reltio AgentFlow MCP Server.

Built on the Strands AI Agents Framework: https://github.com/strands-agents/sdk-python
Learn more at: https://strandsagents.com/
"""

from .client import StrandsReltioClient
from .task import process_prompt

__version__ = "0.1.0"
__all__ = ["StrandsReltioClient", "process_prompt"] 