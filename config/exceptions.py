"""
Simple exceptions for Reltio MCP Strands Client.
"""


class AuthenticationError(Exception):
    """Raised when OAuth 2.0 authentication fails."""
    pass


class ConfigurationError(Exception):
    """Raised when configuration validation fails."""
    pass 