#!/usr/bin/env python3
"""
Simple health check for Reltio AgentFlow MCP Server - Strands Client.

This script provides a straightforward health check for the Strands integration
with Reltio MCP Server. No complex abstractions - just simple, readable code.
"""

import argparse
import logging
import os
import sys

def setup_logging(debug: bool = False) -> None:
    """Setup simple logging."""
    level = logging.INFO if debug else logging.WARNING
    logging.basicConfig(level=level, format='%(message)s')


def run_health_check() -> bool:
    """Run health check and display results."""
    try:
        # Import here to avoid issues if environment is not set up
        from strands_client.client import StrandsReltioClient
        
        print("🔍 Running Reltio MCP Strands Client health check...")
        print("=" * 50)
        
        # Initialize client
        client = StrandsReltioClient()
        
        # Run health check
        status = client.health_check()
        
        print("\n=== Health Check Results ===")
        for key, value in status.items():
            print(f"{key}: {value}")
        
        is_healthy = status.get("status") == "healthy"
        
        if is_healthy:
            print("\n✅ Health check passed - system is healthy!")
        else:
            print("\n❌ Health check failed - system is unhealthy")
        
        return is_healthy
        
    except Exception as e:
        print(f"\n❌ Health check failed with error: {e}")
        return False

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Health check for Reltio MCP Strands Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Run basic health check
  %(prog)s --debug            # Run with debug logging
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
    
    # Run health check
    return 0 if run_health_check() else 1

if __name__ == "__main__":
    sys.exit(main())