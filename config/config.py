"""
Simple configuration for Reltio AgentFlow MCP Server - Strands Client.
"""

import os
from dotenv import load_dotenv


# OAuth endpoint is fixed for Reltio
OAUTH_ENDPOINT = "https://auth.reltio.com/oauth/token"


class Config:
    """Simple configuration class that reads from environment variables."""
    
    def __init__(self, env_file: str = ".env"):
        """Initialize configuration from environment variables."""
        if os.path.exists(env_file):
            load_dotenv(env_file)
        
        # OAuth configuration
        self.oauth_client_id = os.getenv('OAUTH_CLIENT_ID', '')
        self.oauth_client_secret = os.getenv('OAUTH_CLIENT_SECRET', '')
        self.oauth_endpoint = OAUTH_ENDPOINT
        
        # Reltio MCP configuration
        self.tenant_environment = os.getenv('TENANT_ENVIRONMENT', 'dev')
        self.mcp_endpoint = f"https://{self.tenant_environment}.reltio.com/ai/tools/mcp/"
        self.reltio_tenant_id = os.getenv('RELTIO_TENANT_ID', '')
        
        # AI model configuration
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY', '')
        
        # Model settings with defaults
        self.model_temperature = float(os.getenv('MODEL_TEMPERATURE', '0.7'))
        self.model_max_tokens = int(os.getenv('MODEL_MAX_TOKENS', '4096'))
        
        # Model ID selection based on provider
        self._set_model_id()
    
    def _set_model_id(self):
        """Set model ID based on preferred provider."""
        provider = self.get_preferred_model_provider()
        
        if provider == "openai":
            self.model_id = os.getenv('MODEL_ID', 'gpt-4.1')
        elif provider == "anthropic":
            self.model_id = os.getenv('MODEL_ID', 'claude-3-5-sonnet-20241022')
        else:
            # Default fallback
            self.model_id = 'gpt-4.1'
    
    def get_preferred_model_provider(self) -> str:
        """
        Determine the preferred model provider based on available API keys.
        
        Returns:
            str: "openai" or "anthropic" based on available keys.
                 Prefers OpenAI if both are available.
        """
        if self.openai_api_key:
            return "openai"
        elif self.anthropic_api_key:
            return "anthropic"
        else:
            # Default to openai even if no key (will fail gracefully)
            return "openai"

    def get_system_prompt(self) -> str:
        """
        Read the system prompt from system_prompt.txt file.
        
        Returns:
            str: The system prompt content, or a default fallback if file not found.
        """
        try:
            # Try to read from system_prompt.txt in the project root
            prompt_file = os.path.join(os.getcwd(), 'system_prompt.txt')
            if os.path.exists(prompt_file):
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:  # Only return if file has content
                        return content
        except Exception:
            # If anything goes wrong reading the file, fall back to default
            pass
        
        # Fallback to original default
        return "You are a helpful AI assistant with access to Reltio AgentFlow MCP Server tools."


# Global config instance
config = Config() 