"""
Simple OAuth 2.0 Authentication for Reltio AgentFlow MCP Server.
"""

import logging
import time
from typing import Optional

import requests

from .exceptions import AuthenticationError

logger = logging.getLogger(__name__)


class OAuth2Client:
    """Simple OAuth 2.0 Client for Reltio AgentFlow MCP Server authentication."""
    
    def __init__(self, client_id: str, client_secret: str, endpoint: str):
        """Initialize OAuth2 client with credentials.
        
        Args:
            client_id: OAuth client ID
            client_secret: OAuth client secret  
            endpoint: OAuth token endpoint URL
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.endpoint = endpoint
        self._access_token: Optional[str] = None
        self._token_expiry: float = 0
        
    def get_access_token(self) -> str:
        """Get valid access token, refreshing if necessary.
        
        Returns:
            Valid access token
            
        Raises:
            AuthenticationError: If token retrieval fails
        """
        if self._access_token and time.time() < self._token_expiry:
            return self._access_token
            
        try:
            response = requests.post(
                self.endpoint,
                data={
                    'grant_type': 'client_credentials',
                    'client_id': self.client_id,
                    'client_secret': self.client_secret
                },
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                timeout=30
            )
            response.raise_for_status()
            
            token_data = response.json()
            self._access_token = token_data['access_token']
            
            # Set expiry with 5 minute buffer
            expires_in = token_data.get('expires_in', 3600)
            self._token_expiry = time.time() + expires_in - 300
            
            logger.info("OAuth token retrieved successfully")
            return self._access_token
            
        except requests.RequestException as e:
            logger.error(f"Failed to get OAuth token: {e}")
            raise AuthenticationError(f"OAuth token retrieval failed: {e}")
 