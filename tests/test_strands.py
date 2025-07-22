"""
Simple tests for Strands client and CLI modules.
"""

import pytest
import os
import logging
import sys
from unittest.mock import patch, Mock
from strands_client.client import StrandsReltioClient
from config.exceptions import ConfigurationError


def test_strands_client_import():
    """Test that StrandsReltioClient can be imported."""
    # This test just verifies the import works
    assert StrandsReltioClient is not None


@patch('strands_client.client.config')
def test_strands_client_init_fails_without_config(mock_config):
    """Test that client initialization fails without proper configuration."""
    # Mock empty configuration
    mock_config.oauth_client_id = ""
    mock_config.oauth_client_secret = ""
    mock_config.mcp_endpoint = ""
    mock_config.reltio_tenant_id = ""
    
    with pytest.raises(ConfigurationError):
        StrandsReltioClient()


@patch('strands_client.client.config')
@patch('strands_client.client.MCPClient')
@patch('strands_client.client.Agent')
@patch('strands_client.client.OpenAIModel')
def test_strands_client_init_success_openai(mock_openai_model, mock_agent, mock_mcp_client_class, mock_config):
    """Test successful initialization with OpenAI."""
    # Mock config
    mock_config.oauth_client_id = "test_client"
    mock_config.oauth_client_secret = "test_secret"
    mock_config.oauth_endpoint = "https://auth.reltio.com/oauth/token"
    mock_config.mcp_endpoint = "https://dev.reltio.com/ai/tools/mcp/"
    mock_config.reltio_tenant_id = "test_tenant"
    mock_config.openai_api_key = "test_key"
    mock_config.get_preferred_model_provider.return_value = "openai"
    mock_config.model_id = "gpt-4"
    mock_config.model_temperature = 0.7
    mock_config.model_max_tokens = 4096
    
    # Mock OAuth client
    mock_oauth_client = Mock()
    mock_oauth_client.get_access_token.return_value = "test_token"
    
    # Mock MCP client
    mock_mcp_client = Mock()
    mock_mcp_client.list_tools_sync.return_value = [Mock(tool_name="tool1")]
    mock_mcp_client_class.return_value = mock_mcp_client
    
    # This should work without raising exceptions
    client = StrandsReltioClient(oauth_client=mock_oauth_client)
    assert client.mcp_endpoint == "https://dev.reltio.com/ai/tools/mcp/"
    assert client.tenant_id == "test_tenant"


@patch('strands_client.client.config')
@patch('strands_client.client.MCPClient')
@patch('strands_client.client.Agent')
@patch('strands_client.client.AnthropicModel')
def test_strands_client_init_success_anthropic(mock_anthropic_model, mock_agent, mock_mcp_client_class, mock_config):
    """Test successful initialization with Anthropic."""
    # Mock config
    mock_config.oauth_client_id = "test_client"
    mock_config.oauth_client_secret = "test_secret"
    mock_config.oauth_endpoint = "https://auth.reltio.com/oauth/token"
    mock_config.mcp_endpoint = "https://dev.reltio.com/ai/tools/mcp/"
    mock_config.reltio_tenant_id = "test_tenant"
    mock_config.anthropic_api_key = "test_key"
    mock_config.get_preferred_model_provider.return_value = "anthropic"
    mock_config.model_id = "claude-3-5-sonnet"
    mock_config.model_temperature = 0.5
    mock_config.model_max_tokens = 2048
    
    # Mock OAuth client
    mock_oauth_client = Mock()
    mock_oauth_client.get_access_token.return_value = "test_token"
    
    # Mock MCP client
    mock_mcp_client = Mock()
    mock_mcp_client.list_tools_sync.return_value = [Mock(tool_name="tool1")]
    mock_mcp_client_class.return_value = mock_mcp_client
    
    # This should work without raising exceptions
    client = StrandsReltioClient(oauth_client=mock_oauth_client)
    assert client.mcp_endpoint == "https://dev.reltio.com/ai/tools/mcp/"


@patch('strands_client.client.config')
@patch('strands_client.client.OAuth2Client')
def test_strands_client_init_fails_invalid_config(mock_oauth_client_class, mock_config):
    """Test initialization fails when configuration leads to connection errors."""
    # Mock config that will cause MCP connection to fail
    mock_config.oauth_client_id = "invalid_client"
    mock_config.oauth_client_secret = "invalid_secret"
    mock_config.oauth_endpoint = "https://auth.reltio.com/oauth/token"
    mock_config.mcp_endpoint = "https://dev.reltio.com/ai/tools/mcp/"
    mock_config.reltio_tenant_id = "test_tenant"
    mock_config.get_preferred_model_provider.return_value = "openai"
    
    # Mock OAuth client to avoid real requests
    mock_oauth_client = Mock()
    mock_oauth_client_class.return_value = mock_oauth_client
    
    # This should fail during initialization due to invalid credentials
    with pytest.raises(ConfigurationError, match="Initialization failed"):
        StrandsReltioClient()


# Tests for core methods

@patch('strands_client.client.MCPClient')
def test_start_connection_success(mock_mcp_client_class):
    """Test successful MCP connection startup."""
    # Create a mock client without full initialization
    client = StrandsReltioClient.__new__(StrandsReltioClient)
    client._connection_started = False
    client._tools = None
    client._tool_names = []
    
    # Mock OAuth client
    mock_oauth_client = Mock()
    mock_oauth_client.get_access_token.return_value = "test_token"
    client.oauth_client = mock_oauth_client
    
    # Mock MCP client
    mock_mcp_client = Mock()
    mock_tools = [Mock(tool_name="tool1"), Mock(tool_name="tool2")]
    mock_mcp_client.list_tools_sync.return_value = mock_tools
    mock_mcp_client_class.return_value = mock_mcp_client
    
    # Test start_connection
    tools = client.start_connection()
    
    assert tools == mock_tools
    assert client._tools == mock_tools
    assert client._connection_started == True
    assert client._tool_names == ["tool1", "tool2"]


@patch('strands_client.client.OpenAIModel')
@patch('strands_client.client.Agent')
def test_create_agent_success(mock_agent_class, mock_openai_model):
    """Test successful agent creation."""
    # Create a mock client without full initialization
    client = StrandsReltioClient.__new__(StrandsReltioClient)
    client._tools = [Mock(tool_name="tool1")]
    client._agent = None
    
    # Mock config access
    with patch('strands_client.client.config') as mock_config:
        mock_config.get_preferred_model_provider.return_value = "openai"
        mock_config.openai_api_key = "test_key"
        mock_config.model_id = "gpt-4.1"
        mock_config.model_temperature = 0.7
        mock_config.model_max_tokens = 4096
        
        # Mock model and agent
        mock_model = Mock()
        mock_openai_model.return_value = mock_model
        mock_agent = Mock()
        mock_agent_class.return_value = mock_agent
        
        # Test create_agent
        agent = client.create_agent("Custom prompt")
        
        assert agent == mock_agent
        assert client._agent == mock_agent
        mock_agent_class.assert_called_once_with(
            tools=client._tools,
            model=mock_model,
            system_prompt="Custom prompt"
        )


def test_health_check_success():
    """Test successful health check."""
    # Create a mock client without full initialization
    client = StrandsReltioClient.__new__(StrandsReltioClient)
    client.mcp_endpoint = "https://dev.reltio.com/ai/tools/mcp/"
    client.tenant_id = "test_tenant"
    client._tools = [Mock(tool_name="tool1"), Mock(tool_name="tool2")]
    
    # Mock MCP client with successful health check
    mock_mcp_client = Mock()
    mock_mcp_client.call_tool_sync.return_value = {
        'content': [{'text': '{"status": "ok"}'}]
    }
    client._mcp_client = mock_mcp_client
    
    # Test health_check
    status = client.health_check()
    
    assert status["status"] == "healthy"
    mock_mcp_client.call_tool_sync.assert_called_once()


def test_health_check_failure():
    """Test health check with failure."""
    # Create a mock client without full initialization
    client = StrandsReltioClient.__new__(StrandsReltioClient)
    client.mcp_endpoint = "https://dev.reltio.com/ai/tools/mcp/"
    client.tenant_id = "test_tenant"
    client._tools = [Mock(tool_name="tool1")]
    
    # Mock MCP client that raises exception
    mock_mcp_client = Mock()
    mock_mcp_client.call_tool_sync.side_effect = Exception("Health check failed")
    client._mcp_client = mock_mcp_client
    
    # Test health_check
    status = client.health_check()
    
    assert status["status"] == "unhealthy"


def test_process_prompt_success():
    """Test successful prompt processing."""
    # Create a mock client without full initialization
    client = StrandsReltioClient.__new__(StrandsReltioClient)
    
    # Mock agent that returns a response
    mock_agent = Mock()
    mock_agent.return_value = "Agent response to the prompt"
    client._agent = mock_agent
    
    # Test process_prompt
    response = client.process_prompt("Test prompt")
    
    assert response == "Agent response to the prompt"
    mock_agent.assert_called_once_with("Test prompt")


def test_process_prompt_failure():
    """Test prompt processing with failure."""
    # Create a mock client without full initialization
    client = StrandsReltioClient.__new__(StrandsReltioClient)
    
    # Mock agent that raises exception
    mock_agent = Mock()
    mock_agent.side_effect = Exception("Processing failed")
    client._agent = mock_agent
    
    # Test process_prompt should re-raise the exception
    with pytest.raises(Exception, match="Processing failed"):
        client.process_prompt("Test prompt")


def test_strands_client_has_core_methods():
    """Test that StrandsReltioClient has the expected core methods."""
    # Just check the methods exist without calling them
    assert hasattr(StrandsReltioClient, 'process_prompt')
    assert hasattr(StrandsReltioClient, 'health_check')
    assert hasattr(StrandsReltioClient, 'start_connection')
    assert hasattr(StrandsReltioClient, 'create_agent')


# Health Check CLI Tests

def test_health_check_setup_logging():
    """Test health check logging setup."""
    from strands_client.health_check import setup_logging
    
    # Test that the function exists and doesn't crash
    setup_logging(debug=True)
    setup_logging(debug=False)
    # Just test that the function executes without error


@patch.dict(os.environ, {
    'OAUTH_CLIENT_ID': 'test_id',
    'OAUTH_CLIENT_SECRET': 'test_secret',
    'TENANT_ENVIRONMENT': 'dev',
    'RELTIO_TENANT_ID': 'test_tenant',
    'OPENAI_API_KEY': 'test_key'
})
def test_health_check_validate_environment_success():
    """Test successful environment validation."""
    from strands_client.health_check import validate_environment
    
    result = validate_environment()
    assert result is True


@patch.dict(os.environ, {}, clear=True)
def test_health_check_validate_environment_missing_vars():
    """Test environment validation with missing variables."""
    from strands_client.health_check import validate_environment
    
    result = validate_environment()
    assert result is False


def test_health_check_run_success():
    """Test successful health check run."""
    from strands_client.health_check import run_health_check
    
    # Mock client
    mock_client = Mock()
    mock_client.health_check.return_value = {"status": "healthy"}
    
    # Patch the import where it's used
    with patch('strands_client.client.StrandsReltioClient', return_value=mock_client):
        result = run_health_check()
        assert result is True


def test_health_check_run_failure():
    """Test health check run with failure."""
    from strands_client.health_check import run_health_check
    
    # Patch the import where it's used to raise exception
    with patch('strands_client.client.StrandsReltioClient', side_effect=Exception("Connection failed")):
        result = run_health_check()
        assert result is False


@patch('strands_client.health_check.validate_environment')
@patch('sys.argv', ['health_check', '--debug'])
def test_health_check_main_missing_env(mock_validate):
    """Test main function with missing environment."""
    from strands_client.health_check import main
    
    mock_validate.return_value = False
    
    result = main()
    assert result == 1


@patch('strands_client.health_check.validate_environment')
@patch('strands_client.health_check.run_health_check')
@patch('sys.argv', ['health_check'])
def test_health_check_main_success(mock_run_health, mock_validate):
    """Test main function success."""
    from strands_client.health_check import main
    
    mock_validate.return_value = True
    mock_run_health.return_value = True
    
    result = main()
    assert result == 0


# Chat CLI Tests

def test_chat_setup_logging():
    """Test chat logging setup."""
    from strands_client.chat import setup_logging
    
    # Test that the function exists and doesn't crash
    setup_logging(debug=True)
    setup_logging(debug=False)
    # Just test that the function executes without error


@patch.dict(os.environ, {
    'OAUTH_CLIENT_ID': 'test_id',
    'OAUTH_CLIENT_SECRET': 'test_secret',
    'TENANT_ENVIRONMENT': 'dev',
    'RELTIO_TENANT_ID': 'test_tenant',
    'OPENAI_API_KEY': 'test_key'
})
def test_chat_validate_environment_success():
    """Test successful environment validation in chat."""
    from strands_client.chat import validate_environment
    
    result = validate_environment()
    assert result is True


@patch.dict(os.environ, {}, clear=True)
def test_chat_validate_environment_missing_vars():
    """Test environment validation with missing variables in chat."""
    from strands_client.chat import validate_environment
    
    result = validate_environment()
    assert result is False


@patch('builtins.input', side_effect=['quit'])
def test_chat_run_interactive_chat_quit(mock_input):
    """Test interactive chat with quit command."""
    from strands_client.chat import run_interactive_chat
    
    # Mock client
    mock_client = Mock()
    
    with patch('strands_client.client.StrandsReltioClient', return_value=mock_client):
        result = run_interactive_chat()
        assert result == 0


@patch('builtins.input', side_effect=['health', 'quit'])
def test_chat_run_interactive_chat_health_command(mock_input):
    """Test interactive chat with health command."""
    from strands_client.chat import run_interactive_chat
    
    # Mock client
    mock_client = Mock()
    mock_client.health_check.return_value = {"status": "healthy"}
    
    with patch('strands_client.client.StrandsReltioClient', return_value=mock_client):
        result = run_interactive_chat()
        assert result == 0
        mock_client.health_check.assert_called_once()


@patch('builtins.input', side_effect=['test prompt', 'quit'])
def test_chat_run_interactive_chat_prompt(mock_input):
    """Test interactive chat with user prompt."""
    from strands_client.chat import run_interactive_chat
    
    # Mock client
    mock_client = Mock()
    mock_client.process_prompt.return_value = "Agent response"
    
    with patch('strands_client.client.StrandsReltioClient', return_value=mock_client):
        result = run_interactive_chat()
        assert result == 0
        mock_client.process_prompt.assert_called_once_with("test prompt")


def test_chat_run_interactive_chat_init_failure():
    """Test interactive chat with client initialization failure."""
    from strands_client.chat import run_interactive_chat
    
    # Mock client that raises exception during initialization
    with patch('strands_client.client.StrandsReltioClient', side_effect=Exception("Init failed")):
        result = run_interactive_chat()
        assert result == 1


@patch('strands_client.chat.validate_environment')
@patch('sys.argv', ['chat', '--debug'])
def test_chat_main_missing_env(mock_validate):
    """Test chat main function with missing environment."""
    from strands_client.chat import main
    
    mock_validate.return_value = False
    
    result = main()
    assert result == 1


@patch('strands_client.chat.validate_environment')
@patch('strands_client.chat.run_interactive_chat')
@patch('sys.argv', ['chat'])
def test_chat_main_success(mock_run_chat, mock_validate):
    """Test chat main function success."""
    from strands_client.chat import main
    
    mock_validate.return_value = True
    mock_run_chat.return_value = 0
    
    result = main()
    assert result == 0
