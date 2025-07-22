"""
Simple tests for configuration and authentication.
"""

import os
import pytest
from unittest.mock import patch

from config.config import Config, OAUTH_ENDPOINT
from config.auth import OAuth2Client
from config.exceptions import ConfigurationError, AuthenticationError


# Configuration Tests

def test_config_basic_functionality():
    """Test basic config functionality."""
    config = Config()
    
    # Test that it doesn't crash
    assert config is not None
    assert config.oauth_endpoint == OAUTH_ENDPOINT


@patch.dict(os.environ, {
    'OAUTH_CLIENT_ID': 'test_client',
    'TENANT_ENVIRONMENT': 'dev',
    'MODEL_TEMPERATURE': '0.5',
    'MODEL_MAX_TOKENS': '2048'
})
def test_config_reads_environment_variables():
    """Test that config reads environment variables correctly."""
    config = Config()
    
    assert config.oauth_client_id == 'test_client'
    assert config.tenant_environment == 'dev'
    assert config.mcp_endpoint == 'https://dev.reltio.com/ai/tools/mcp/'
    assert config.model_temperature == 0.5
    assert config.model_max_tokens == 2048


@patch.dict(os.environ, {'OPENAI_API_KEY': 'openai_key'})
def test_preferred_model_provider():
    """Test model provider selection."""
    config = Config()
    assert config.get_preferred_model_provider() == "openai"


@patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'anthropic_key', 'OPENAI_API_KEY': ''}, clear=True)
def test_preferred_model_provider_anthropic():
    """Test model provider selection with Anthropic."""
    config = Config()
    assert config.get_preferred_model_provider() == "anthropic"


# Authentication Tests

def test_oauth_client_creation():
    """Test OAuth2Client can be created with correct attributes."""
    client = OAuth2Client(
        client_id="test_client",
        client_secret="test_secret",
        endpoint="https://auth.example.com/token"
    )
    
    assert client.client_id == "test_client"
    assert client.client_secret == "test_secret"
    assert client.endpoint == "https://auth.example.com/token"


def test_oauth_client_has_required_attributes():
    """Test that OAuth2Client has the expected attributes."""
    client = OAuth2Client("id", "secret", "endpoint")
    
    # Test that it has the required attributes
    assert hasattr(client, '_access_token')
    assert hasattr(client, '_token_expiry')
    assert hasattr(client, 'get_access_token')
    
    # Test initial state
    assert client._access_token is None
    assert client._token_expiry == 0


# System Prompt Tests

def test_get_system_prompt_fallback():
    """Test that get_system_prompt returns default when file doesn't exist."""
    config = Config()
    
    # When system_prompt.txt doesn't exist, should return default
    with patch('os.path.exists', return_value=False):
        prompt = config.get_system_prompt()
        assert "helpful AI assistant" in prompt
        assert "Reltio AgentFlow MCP Server tools" in prompt


def test_get_system_prompt_from_file():
    """Test that get_system_prompt reads from file when it exists."""
    config = Config()
    
    # Mock file content
    mock_content = "Custom system prompt for testing"
    
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', create=True) as mock_open:
        
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.read.return_value = mock_content
        
        prompt = config.get_system_prompt()
        assert prompt == mock_content


def test_get_system_prompt_empty_file():
    """Test that get_system_prompt falls back to default when file is empty."""
    config = Config()
    
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', create=True) as mock_open:
        
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.read.return_value = "   "  # Empty/whitespace content
        
        prompt = config.get_system_prompt()
        assert "helpful AI assistant" in prompt
        assert "Reltio AgentFlow MCP Server tools" in prompt
