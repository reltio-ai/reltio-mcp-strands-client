#!/usr/bin/env python3
"""
Simple task processor for Reltio AgentFlow MCP Server - Strands Client.

This module provides a simple function to process a single prompt using
Strands agents with access to Reltio AgentFlow MCP Server tools.
"""

import sys
from strands_client.client import StrandsReltioClient

def process_prompt(prompt: str) -> str:
    """
    Process a single prompt and return the response.
    
    Uses the same system prompt structure as the chat interface,
    automatically enforcing the tenant_id for MCP tool executions.
    
    Args:
        prompt: The prompt/task to process
        
    Returns:
        str: The agent's response
        
    Raises:
        Exception: If client initialization or prompt processing fails
    """
    # Initialize client (already handles system prompt and tenant_id enforcement)
    client = StrandsReltioClient()
    
    # Process the prompt and return response
    response = client.process_prompt(prompt)
    return response

def main():
    """Command-line interface."""
    if len(sys.argv) != 2:
        print("Usage: python strands_client/task.py \"<your prompt>\"")
        print("Example: python strands_client/task.py \"Get entity summary for entity ID 123\"")
        sys.exit(1)
    
    prompt = sys.argv[1]
    
    try:
        response = process_prompt(prompt)
        print(response)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 