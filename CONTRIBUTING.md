# Contributing to Reltio MCP Strands Client

Thank you for your interest in contributing to the Reltio MCP Strands Client! This project serves as sample code for Reltio partners and customers to integrate with Reltio's AgentFlow MCP Server using the [Strands AI Agents Framework](https://github.com/strands-agents/sdk-python).

## Code of Conduct

This project adheres to Reltio's commitment to providing a welcoming and inclusive environment for all contributors. Please be respectful and professional in all interactions.

## How to Contribute

### Reporting Issues

If you encounter bugs or have feature requests:

1. Check if the issue already exists in the [GitHub Issues](https://github.com/reltio-ai/reltio-mcp-strands-client/issues)
2. If not, create a new issue with:
   - Clear description of the problem or enhancement
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Environment details (Python version, OS, etc.)

### Suggesting Enhancements

We welcome suggestions for improvements! Please:

1. Open an issue with the `enhancement` label
2. Describe the use case and expected benefits
3. Consider if this aligns with the project's sample code purpose

### Code Contributions

#### Prerequisites

- Python 3.10 or higher
- Git

#### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/reltio-mcp-strands-client.git
   cd reltio-mcp-strands-client
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

#### Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following our coding standards:
   - Follow PEP 8 style guidelines
   - Add type hints to new functions
   - Include docstrings for public methods
   - Add appropriate logging
   - Handle errors gracefully

3. Write or update tests:
   ```bash
   pytest tests/
   ```

4. Run code quality checks:
   ```bash
   ruff check .
   black .
   mypy .
   ```

5. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: description of your change"
   ```

#### Commit Message Format

Use conventional commits format:
- `feat:` new features
- `fix:` bug fixes  
- `docs:` documentation changes
- `test:` test additions or modifications
- `refactor:` code refactoring
- `style:` formatting changes

#### Pull Request Process

1. Push your branch to your fork
2. Create a Pull Request with:
   - Clear title and description
   - Reference any related issues
   - Include testing instructions
   - Ensure all CI checks pass

3. Address review feedback promptly
4. Maintain a clean commit history

## Development Guidelines

### Code Style

- Use Black for code formatting (line length: 88)
- Follow Ruff linting rules
- Use meaningful variable and function names
- Keep functions focused and small

### Testing

- Write unit tests for new functionality
- Maintain test coverage above 80%
- Use mocking for external dependencies
- Include both positive and negative test cases

### Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Include examples in docstrings where helpful
- Keep documentation concise but complete

## Project Scope

This project is intended as **sample code** for Reltio partners and customers. Contributions should:

- Enhance clarity and educational value
- Improve integration patterns
- Fix bugs or security issues
- Add helpful examples

Avoid contributions that:
- Add complex enterprise features
- Include production-specific configurations
- Create extensive abstractions

## Getting Help

- Check the README.md for basic usage questions
- Review existing issues and discussions
- For Strands Framework questions, visit [strandsagents.com](https://strandsagents.com/) or the [Strands repository](https://github.com/strands-agents/sdk-python)
- For Reltio-specific questions, contact your Reltio representative

## License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 License.

---

Thank you for helping make this sample code better for the Reltio community! 