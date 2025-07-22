# Reltio AgentFlow MCP Server - Strands Client

A minimalistic Python client for connecting [Strands AI agents](https://strandsagents.com/) to Reltio AgentFlow MCP Server with OAuth 2.0 authentication.

Built on top of the [Strands AI Agents Framework](https://github.com/strands-agents/sdk-python) - a model-driven approach to building AI agents with native MCP (Model Context Protocol) support.

## Prerequisites

### Technical Requirements
- Python 3.10 or higher
- OpenAI or Anthropic API key

### Reltio AgentFlow MCP Server Access

**Important**: To connect to Reltio AgentFlow MCP Server, you must meet ALL of the following requirements:

1. **MCP Customer Status**: Your organization must be a Reltio AgentFlow MCP Server customer. Without this, you will not be able to reach the MCP server endpoints.

2. **MCP-Enabled Tenant**: The specific Reltio tenant(s) you want to use must be enabled for MCP access. This happens when you purchase Reltio AgentFlow MCP Server and is configured by Reltio.

3. **Proper Client Credentials**: Your OAuth client credentials must have the following role assignment:
   - `ROLE_EXECUTE_MCP["tenant_id"]` - Required to execute any MCP operations on the specified tenant
   - **Additional tenant-specific permissions** for the operations you want to perform, such as:
     - `MDM.entities.READ` - To read entities via MCP
     - `MDM.entities.WRITE` - To create/update entities via MCP
     - `MDM.relations.READ` - To read relationships via MCP
     - Other relevant permissions based on your use case

### Getting Access

If you don't have access to Reltio AgentFlow MCP Server:
- Contact your Reltio account representative
- Visit [Reltio's website](https://www.reltio.com/) for more information about AgentFlow MCP Server

## Installation

### For Running the Application

```bash
git clone git@github.com:reltio-ai/reltio-mcp-strands-client.git
cd reltio-mcp-strands-client
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install only runtime dependencies
pip install -r requirements.txt
```

### For Development

```bash
git clone git@github.com:reltio-ai/reltio-mcp-strands-client.git
cd reltio-mcp-strands-client
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install runtime + development dependencies
pip install -r requirements-dev.txt

# Or alternatively, install in editable mode with dev dependencies
pip install -e .[dev]
```

## Configuration

Create a `.env` file with your credentials:

```bash
# Reltio OAuth Configuration
OAUTH_CLIENT_ID=your_oauth_client_id
OAUTH_CLIENT_SECRET=your_oauth_client_secret

# Reltio MCP Configuration
TENANT_ENVIRONMENT=dev  # or test, prod-usg, etc.
RELTIO_TENANT_ID=your_tenant_id

# AI Model Configuration (at least one required)
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional Model Settings
MODEL_TEMPERATURE=0.7
MODEL_MAX_TOKENS=4096
```

### System Prompt Customization

The system prompt is configurable via the `system_prompt.txt` file in the project root. You can modify this file to customize how the AI assistant behaves:

```txt
You are a helpful AI assistant with access to Reltio MCP AgentFlow MCP Server tools.

You can help users with:
- Data queries and analysis using Reltio's MCP tools
- Entity relationship exploration
- Data quality assessment
- Business insights and recommendations

Always be clear, concise, and helpful in your responses.
```

## Core Functionalities

### Health Check

Verify the connection to Reltio AgentFlow MCP Server.

```bash
# Basic health check
reltio-mcp-strands-health

# With debug logging
reltio-mcp-strands-health --debug
```

### Interactive Chat

Start an interactive chat session to send prompts and receive responses using MCP tools.

```bash
# Start interactive chat
reltio-mcp-strands-chat

# With debug logging
reltio-mcp-strands-chat --debug
```

In chat mode, you can:
- Send natural language prompts
- Type `health` to check system status
- Type `quit` or `exit` to end the session

### Single Task Processing

Process a single prompt and get a response without interactive chat.

```bash
# Process a single task
reltio-mcp-strands-task "Get entity summary for entity ID 123"

# Another example
reltio-mcp-strands-task "Search for entities with name containing 'John'"
```

This is ideal for:
- Building AI Agents that connect to Reltio AgentFlow MCP Server
- Scripting and automation
- Batch processing
- Integration with other tools
- One-off queries

## Python API

### Using the Client Directly

```python
from strands_client.client import StrandsReltioClient

# Initialize client
client = StrandsReltioClient()

# Process prompts
response = client.process_prompt("Your prompt here")

# Check health
status = client.health_check()
```

### Using the Simple Task Function

```python
from strands_client import process_prompt

# Simple one-line usage
response = process_prompt("Get entity summary for entity ID 123")
print(response)
```

## ⚠️ Security Considerations

**Important**: This is a **thin client** that provides direct access to Large Language Models (LLMs) without built-in guardrails or safety mechanisms. 

### Key Points

- **No Guardrails**: This sample client does not implement input validation, output filtering, or content safety measures
- **Direct LLM Access**: User prompts are passed directly to the configured LLM (OpenAI/Anthropic) with minimal processing
- **Production Responsibility**: If you deploy agents based on this code in production, **you are responsible for implementing**:
  - Input sanitization and validation
  - Output filtering and safety checks
  - Rate limiting and abuse prevention
  - User authentication and authorization
  - Audit logging and monitoring
  - Content safety and compliance measures

### For Production Use

Before using this code as a foundation for production systems:

1. **Review our [Security Policy](SECURITY.md)** for comprehensive security guidelines
2. **Implement appropriate guardrails** for your specific use case and regulatory requirements
3. **Add safety measures** such as content filtering, input validation, and output sanitization
4. **Consider security frameworks** like OWASP guidelines for AI systems
5. **Test thoroughly** with adversarial inputs and edge cases

This sample code is intended for **educational and integration purposes** to demonstrate Reltio MCP integration patterns using the Strands framework.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=strands_client --cov=config

# Verbose output
pytest -v
```

## Project Structure

```
├── config/                 # Configuration and authentication
├── strands_client/         # Main client and CLI tools
├── tests/                  # Test suite
├── system_prompt.txt       # Configurable AI assistant prompt
├── requirements.txt        # Runtime dependencies
├── requirements-dev.txt    # Development dependencies
└── pyproject.toml         # Project configuration
```

## About Strands AI Agents

This client is built on the [Strands AI Agents Framework](https://github.com/strands-agents/sdk-python), an open-source Python framework for building AI agents with:

- **Native MCP Support**: Built-in Model Context Protocol integration
- **Multi-Provider Support**: Works with OpenAI, Anthropic, Amazon Bedrock, and more
- **Tool Integration**: Seamless connection to external APIs and services
- **Flexible Architecture**: Model-driven approach with minimal code

Learn more at [strandsagents.com](https://strandsagents.com/)

## Acknowledgments

- [Strands AI Agents Framework](https://github.com/strands-agents/sdk-python) - The foundational framework powering this integration
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) - The protocol enabling seamless tool integration

## License

Apache 2.0 License - see the LICENSE file for details. 
