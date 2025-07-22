# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-07-22

### Added
- Initial release of Reltio MCP Strands Client
- OAuth 2.0 authentication for Reltio AgentFlow MCP Server
- Integration with [Strands AI Agents Framework](https://github.com/strands-agents/sdk-python) with native MCP support
- Interactive chat CLI (`reltio-mcp-strands-chat`)
- Health check CLI (`reltio-mcp-strands-health`)
- Support for OpenAI and Anthropic models
- Configurable system prompts via `system_prompt.txt`
- Comprehensive test suite with pytest
- Environment-based configuration with `.env` support
- Error handling with custom exceptions
- Type hints and mypy configuration
- Code quality tools (ruff, black, isort)
- Apache 2.0 license
- Comprehensive documentation

### Security
- HTTPS-only communications
- OAuth 2.0 token management with automatic refresh
- Environment variable-based credential management
- Input validation for CLI commands
- Secure error handling without credential exposure

### Documentation
- Complete README with installation and usage instructions
- API documentation with examples
- Configuration guide
- Testing instructions
- License and attribution files

---

## Release Process

### Version Numbering
- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
- **MAJOR**: Breaking changes to API or behavior
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Types
- **Alpha** (0.x.x): Initial development, may have breaking changes
- **Beta** (1.0.0-beta.x): Feature complete, testing phase
- **Stable** (1.0.0+): Production ready

### What's Not Versioned
Since this is sample code:
- Configuration examples may change without version bumps
- Documentation improvements are continuous
- Minor CLI output changes don't require version updates

### Support Policy
- **Current version**: Full support and updates
- **Previous minor version**: Security fixes only
- **Sample code**: Educational purpose, not production support 