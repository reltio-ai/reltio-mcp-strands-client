"""
Strands AI Agents Framework Integration for Reltio AgentFlow MCP Server.

This module provides native MCP integration using the Strands AI Agents Framework,
leveraging Strands' built-in MCP support for seamless tool integration.

Strands Framework: https://github.com/strands-agents/sdk-python
Official Site: https://strandsagents.com/
"""

import json
import logging
import uuid
from typing import Optional, Dict, Any, List
from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient
from strands.models.openai import OpenAIModel
from strands.models.anthropic import AnthropicModel

from config import config, OAuth2Client, ConfigurationError

logger = logging.getLogger(__name__)


class StrandsReltioClient:
    """Client for integrating Strands framework with Reltio MCP Clients."""
    
    def __init__(self, oauth_client: Optional[OAuth2Client] = None):
        """Initialize Strands Reltio client.
        
        Args:
            oauth_client: OAuth2Client instance (optional, will create from config if None)
        """
        self.oauth_client = oauth_client or OAuth2Client(
            client_id=config.oauth_client_id,
            client_secret=config.oauth_client_secret,
            endpoint=config.oauth_endpoint
        )
        
        self.mcp_endpoint = config.mcp_endpoint
        self.tenant_id = config.reltio_tenant_id
        
        if not all([self.mcp_endpoint, self.tenant_id]):
            raise ConfigurationError("Missing required MCP configuration")
        
        self._agent: Optional[Agent] = None
        self._mcp_client: Optional[MCPClient] = None
        self._tools: Optional[List] = None
        self._tool_names: List[str] = []
        self._connection_started: bool = False
        
        logger.info("StrandsReltioClient initialized - starting connections...")
        
        # Establish connections immediately during initialization
        try:
            self.start_connection()
            self.create_agent()
            logger.info("StrandsReltioClient ready for use")
        except Exception as e:
            logger.error(f"Failed to initialize StrandsReltioClient: {e}")
            raise ConfigurationError(f"Initialization failed: {e}")
    
    def _create_mcp_transport(self):
        """Create MCP transport with authentication headers."""
        token = self.oauth_client.get_access_token()
        
        # Create a transport callable that includes authentication headers
        def transport_callable():
            return streamablehttp_client(
                self.mcp_endpoint,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            )
        
        return transport_callable
    
    def _create_model(self):
        """Create appropriate model object based on configuration.
        
        Returns:
            Configured model object (OpenAIModel or AnthropicModel)
            
        Raises:
            ConfigurationError: If no valid API key is found
        """
        provider = config.get_preferred_model_provider()
        model_id = config.model_id
        temperature = config.model_temperature
        max_tokens = config.model_max_tokens
        
        if provider == "openai":
            logger.info(f"Creating OpenAI model: {model_id} (max_tokens: {max_tokens}, temperature: {temperature})")
            return OpenAIModel(
                client_args={
                    "api_key": config.openai_api_key,
                },
                model_id=model_id,
                params={
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                }
            )
        elif provider == "anthropic":
            logger.info(f"Creating Anthropic model: {model_id} (max_tokens: {max_tokens}, temperature: {temperature})")
            return AnthropicModel(
                client_args={
                    "api_key": config.anthropic_api_key,
                },
                max_tokens=max_tokens,
                model_id=model_id,
                params={
                    "temperature": temperature,
                }
            )
        else:
            raise ConfigurationError("No valid API key found. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable.")
    
    def start_connection(self) -> List:
        """Start MCP connection and retrieve tools.
        
        Returns:
            List of MCP tools wrapped as AgentTools
        """
        if self._connection_started:
            logger.info("MCP connection already started")
            return self._tools
            
        try:
            transport_callable = self._create_mcp_transport()
            
            # Create MCP client
            self._mcp_client = MCPClient(transport_callable)
            
            # Start the connection and get tools
            self._mcp_client.start()  # Start the background thread
            tools = self._mcp_client.list_tools_sync()
            self._tools = tools
            
            # Extract and store tool names for easy access
            self._tool_names = [tool.tool_name for tool in tools] if tools else []
            
            self._connection_started = True
            print(f"MCP connection started with {len(tools)} tools.")
            logger.info(f"MCP connection started with {len(tools)} tools.")
            return tools
                
        except Exception as e:
            logger.error(f"Failed to start MCP connection: {e}")
            raise ConfigurationError(f"MCP setup failed: {e}")
      
    def create_agent(self, system_prompt: str = None) -> Agent:
        """
        Create an agent with the configured model and MCP tools.
        
        Args:
            system_prompt: Optional custom system prompt. If not provided, 
                          will read from system_prompt.txt file or use default.
        
        Returns:
            Agent: Configured agent ready for processing prompts.
        """
        # Connection is already established during initialization
        model = self._create_model()
        prompt = system_prompt or config.get_system_prompt()
        prompt += f"\n\n For all MCP tool executions, you must use {self.tenant_id} as the tenant_id of the tool input."
        # Create agent with configurable system prompt
        self._agent = Agent(
            tools=self._tools,
            model=model,
            system_prompt=prompt,
        )
        
        logger.info("Strands agent created successfully")
        return self._agent
    
    def process_prompt(self, prompt: str) -> str:
        """Process a prompt using the Strands agent.
        
        Args:
            prompt: User prompt to process
            
        Returns:
            Agent response
        """
        try:
            # Agent and connection are already established during initialization
            response = self._agent(prompt)
            return str(response)
        except Exception as e:
            logger.error(f"Failed to process prompt: {e}")
            raise
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check of the integration.
        
        Returns:
            Health status information
        """
        try:
            result = self._mcp_client.call_tool_sync(f"health-check-{uuid.uuid4()}", "health_check", {})
            health_data = json.loads(result.get('content', [{}])[0].get('text', '{}'))
            return {"status": "healthy" if health_data.get('status') == 'ok' else "unhealthy"}
        except Exception:
            return {"status": "unhealthy"}
 