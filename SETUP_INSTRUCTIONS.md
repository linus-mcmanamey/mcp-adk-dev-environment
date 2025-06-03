# MCP ADK Development Environment Setup Instructions

This repository provides a complete Model Context Protocol (MCP) development environment with Google ADK Python framework integration and custom network discovery capabilities.

## Quick Start

### 1. Clone this Repository

```bash
git clone https://github.com/linus-mcmanamey/mcp-adk-dev-environment.git
cd mcp-adk-dev-environment
```

### 2. Set Up ADK Repositories

The Google ADK repositories are not included in this repo due to size. Clone them separately:

```bash
# Clone Google ADK Python repository
git clone https://github.com/google/adk-python.git

# Clone Google ADK Documentation repository  
git clone https://github.com/google/adk-docs.git
```

### 3. Configure Environment Variables

Copy the example environment file and configure your API keys:

```bash
cp .env .env.local
# Edit .env.local with your actual API keys
```

### 4. Install Dependencies

```bash
# Install main project dependencies
pip install -r requirements.txt

# Install network discovery MCP server
cd network_discovery_mcp
pip install -e .
cd ..
```

### 5. Test MCP Servers

```bash
# Make scripts executable
chmod +x *.sh

# Test MCP server configuration
./test-mcp-servers.sh

# Test network discovery functionality
./test-network-discovery.sh
```

### 6. Start MCP Servers

```bash
./start-mcp-servers.sh
```

## What's Included

### MCP Servers

- **Filesystem Server**: Provides access to local files and directories
- **Network Discovery Server**: Custom server for network device identification

### Documentation

- `MCP_PYTHON_REPOSITORY_GUIDE.md` - General MCP setup guide
- `ADK_COMPLETE_SETUP.md` - Comprehensive ADK setup documentation
- `NETWORK_DISCOVERY_MCP_SETUP.md` - Network discovery server documentation

### Google ADK Integration

- Pre-configured MCP access to ADK Python source code
- Access to ADK documentation and examples
- Ready-to-use development environment

### Development Tools

- Dev container configuration for consistent environments
- Pre-commit hooks for code quality
- Testing scripts for validation
- Comprehensive project structure

## Usage with AI Assistants

This environment is designed to provide AI assistants with comprehensive access to:

1. **Google ADK Framework**: Complete source code, documentation, and examples
2. **Network Discovery**: Tools for identifying and analyzing network devices
3. **Development Context**: Project structure, dependencies, and configuration

The MCP servers enable AI assistants to:

- Browse and analyze ADK source code
- Access ADK documentation and tutorials
- Perform network discovery and device identification
- Understand project structure and dependencies

## Repository Structure

```
├── mcp-config.json           # MCP server configuration
├── network_discovery_mcp/    # Custom network discovery MCP server
├── adk-python/              # Google ADK Python (clone separately)
├── adk-docs/                # Google ADK docs (clone separately)
├── *.md                     # Documentation files
├── *.sh                     # Utility scripts
└── .devcontainer/           # Development container config
```

## Troubleshooting

### MCP Server Issues

1. Check that all dependencies are installed
2. Verify file paths in `mcp-config.json`
3. Test individual servers using the test scripts

### ADK Repository Access

1. Ensure repositories are cloned in the correct locations
2. Check MCP configuration includes the repository paths
3. Verify semantic search can access the content

### Network Discovery Issues

1. Some features require `nmap` (install with: `sudo apt install nmap`)
2. Ping functionality may require system permissions
3. Check network connectivity and firewall settings

## Contributing

See `CONTRIBUTING.md` in the Google ADK repositories for contribution guidelines.

## License

This project configuration is provided under the same license terms as the Google ADK framework.
