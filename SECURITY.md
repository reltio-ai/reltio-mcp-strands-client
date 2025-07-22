# Security Policy

## Supported Versions

This project is sample code intended for educational and integration purposes. Security updates will be provided for:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

Reltio takes security seriously. If you discover a security vulnerability in this sample code, please help us resolve it responsibly.

### Reporting Process

**Do NOT create a public GitHub issue for security vulnerabilities.**

Instead, please:

1. **Email**: Send details to `security@reltio.com`
2. **Subject**: Include "Security Vulnerability - MCP Strands Client" in the subject line
3. **Details**: Include as much information as possible:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment**: We'll acknowledge receipt within 48 hours
- **Assessment**: Initial assessment within 5 business days
- **Resolution**: We'll work to resolve confirmed vulnerabilities promptly
- **Disclosure**: Coordinated disclosure after the issue is resolved

### Security Best Practices

When using this sample code:

#### Credential Management
- **Never commit credentials** to version control
- Use environment variables or secure credential stores
- Rotate OAuth credentials regularly
- Use least-privilege access principles

#### Production Considerations
- This is **sample code** - not production-ready
- Implement additional security measures for production use:
  - Input validation and sanitization
  - Rate limiting
  - Proper error handling without information disclosure
  - Security logging and monitoring

#### Network Security
- Use HTTPS for all API communications
- Validate SSL certificates
- Consider network segmentation for production deployments

#### Dependencies
- Regularly update dependencies to latest secure versions
- Monitor security advisories for dependencies
- Use tools like `pip-audit` to check for known vulnerabilities

### Scope

This security policy covers:
- The sample client code
- Configuration and authentication patterns
- Documentation examples

This policy does NOT cover:
- Third-party dependencies (report to respective maintainers)
- Reltio's production services (use standard Reltio security channels)
- Issues in user implementations based on this sample

### Security Features

This sample includes:
- OAuth 2.0 authentication with token refresh
- HTTPS-only communications
- Environment-based configuration
- Input validation for CLI commands
- Proper error handling without credential exposure

### Additional Resources

- [Reltio Documentation](https://docs.reltio.com/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP GenAI Security Project](https://genai.owasp.org/)
- [Python Security Guidelines](https://python.org/dev/security/)

---

Thank you for helping keep Reltio and our community secure! 