#!/usr/bin/env python3
"""
Interactive chat for Reltio AgentFlow MCP Server - Strands Client.

This script provides a simple interactive chat interface for communicating with 
Strands agents that have access to Reltio AgentFlow MCP Server tools.
No complex abstractions - just simple, readable code.
"""

import argparse
import logging
import os
import sys

def setup_logging(debug: bool = False) -> None:
    """Setup simple logging."""
    level = logging.INFO if debug else logging.WARNING
    logging.basicConfig(level=level, format='%(message)s')



def run_interactive_chat() -> int:
    """Run interactive chat loop."""
    try:
        # Import here to avoid issues if environment is not set up
        from strands_client.client import StrandsReltioClient
        
        print("🔄 Initializing Reltio MCP Strands Client...")
        client = StrandsReltioClient()
        print("✅ Client ready!\n")
        
        print("🤖 Reltio MCP Chat - Strands Framework")
        print("=" * 50)
        print("Welcome to the interactive chat with Reltio MCP AgentFlow!")
        print("Type your questions or requests below.")
        print("Commands: 'quit', 'exit' to stop | 'health' for health check | 'clear' to clear screen")
        print("=" * 50)
        
        while True:
            try:
                prompt = input("\n💬 You: ").strip()
                
                if prompt.lower() in ['quit', 'exit']:
                    print("\n👋 Goodbye!")
                    break
                elif prompt.lower() == 'health':
                    print("\n🔍 Running health check...")
                    status = client.health_check()
                    health_status = status.get("status", "unknown")
                    if health_status == "healthy":
                        print("✅ System is healthy")
                    elif health_status == "partial":
                        print("⚠️ System is partially healthy")
                    else:
                        print("❌ System is unhealthy")
                    continue
                elif prompt.lower() == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue
                elif not prompt:
                    continue
                
                print("\n🤔 Agent is thinking...")        
                try:
                    client.process_prompt(prompt)
                except Exception as e:
                    print(f"\n❌ Error processing prompt: {e}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Chat interrupted. Goodbye!")
                break
            except EOFError:
                print("\n\n👋 Chat ended. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Failed to start chat: {e}")
        return 1

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Interactive chat for Reltio MCP Strands Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Start interactive chat
  %(prog)s --debug            # Start with debug logging
        """
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.debug)
    
    # Run interactive chat
    return run_interactive_chat()

if __name__ == "__main__":
    sys.exit(main()) 