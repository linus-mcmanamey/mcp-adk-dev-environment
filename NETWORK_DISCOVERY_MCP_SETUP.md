# Complete MCP Setup with Network Discovery

This document provides a comprehensive guide to your MCP (Model Context Protocol) setup including Google ADK repositories and custom network discovery capabilities.

## Overview

Your MCP configuration now includes three powerful servers:

1. **Filesystem Server** - Access to Google ADK Python code and documentation
2. **GitHub Server** - GitHub repository integration
3. **Network Discovery Server** - Custom local network device discovery

## MCP Servers Configuration

### 1. Filesystem Server

**Purpose**: Provides AI assistants with access to Google ADK Python framework source code and documentation.

**Configuration**:

```json
"filesystem": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem"],
  "env": {
    "ALLOWED_DIRECTORIES": "/workspaces,/workspaces/adk_dev_trial/adk-python,/workspaces/adk_dev_trial/adk-docs"
  }
}
```

**Capabilities**:

- Read Google ADK Python source code
- Access API documentation and examples
- Browse tutorials and guides
- Explore test cases and sample implementations

### 2. GitHub Server

**Purpose**: Direct integration with GitHub repositories for enhanced development workflow.

**Configuration**:

```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
  }
}
```

**Requirements**: Set `GITHUB_TOKEN` environment variable with your GitHub personal access token.

### 3. Network Discovery Server (Custom)

**Purpose**: Local area network device discovery and identification for ADK agent development.

**Configuration**:

```json
"network-discovery": {
  "command": "python",
  "args": ["-m", "network_discovery_mcp.server"],
  "cwd": "/workspaces/adk_dev_trial/network_discovery_mcp",
  "env": {}
}
```

## Network Discovery Server Features

### Available Tools

1. **scan_network**
   - Scan a network range for active devices
   - Parameters: `network` (CIDR notation), `include_ports` (boolean)
   - Example: `{"network": "192.168.1.0/24", "include_ports": true}`

2. **get_network_interfaces**
   - List local network interfaces
   - No parameters required
   - Returns interface details including IP, netmask, and network range

3. **scan_device_ports**
   - Scan specific ports on a target device
   - Parameters: `host` (IP/hostname), `ports` (optional list)
   - Example: `{"host": "192.168.1.1", "ports": [22, 80, 443]}`

4. **get_device_details**
   - Get comprehensive device information
   - Parameters: `ip_address`
   - Returns device type, services, and connection details

5. **ping_host**
   - Test host reachability
   - Parameters: `host`, `timeout` (optional)
   - Returns connectivity status and response time

6. **discover_local_network**
   - Automatically discover and scan local networks
   - Parameters: `include_ports` (optional boolean)
   - Comprehensive network discovery and device identification

### Device Type Identification

The network discovery server can identify various device types based on open ports:

- **Web Servers** (ports 80, 443)
- **Linux Servers** (SSH on port 22)
- **Windows Computers** (ports 135, 139)
- **Routers/Gateways** (telnet, web, DNS)
- **Network Printers** (ports 631, 9100)
- **RDP Servers** (port 3389)
- **VNC Servers** (port 5900)

## Setup Instructions

### Prerequisites

1. Node.js and npm installed
2. Python 3.10+ with required packages
3. GitHub personal access token (for GitHub server)

### Installation Steps

1. **Install Network Discovery MCP Server**:

   ```bash
   cd /workspaces/adk_dev_trial/network_discovery_mcp
   pip install -e .
   ```

2. **Set Environment Variables**:

   ```bash
   export GITHUB_TOKEN="your_github_personal_access_token"
   ```

3. **Test MCP Configuration**:

   ```bash
   cd /workspaces/adk_dev_trial
   ./test-mcp-servers.sh
   ```

4. **Start MCP Servers**:

   ```bash
   ./start-mcp-servers.sh
   ```

## Usage Examples

### AI Assistant Integration

With this MCP setup, AI assistants can now:

1. **Analyze Google ADK Code**:
   - "Show me how to create a custom agent using the Google ADK"
   - "Find examples of tool implementations in the ADK Python codebase"
   - "Explain the ADK session management architecture"

2. **GitHub Integration**:
   - "Check the latest commits in the Google ADK repository"
   - "Create issues and pull requests"
   - "Search across multiple repositories"

3. **Network Discovery**:
   - "Scan my local network for devices"
   - "Identify what services are running on device 192.168.1.100"
   - "Find all web servers on my network"
   - "Create a network topology map"

### Development Workflow

**For ADK Agent Development**:

1. Use filesystem server to explore ADK examples
2. Use network discovery to identify target devices for agent deployment
3. Use GitHub server to manage code and documentation
4. Leverage all three for comprehensive development support

## Network Discovery Use Cases

### ADK Agent Scenarios

- **IoT Device Management**: Discover and catalog IoT devices for agent interaction
- **Home Automation**: Identify smart home devices and their capabilities
- **Network Security**: Monitor network changes and new device connections
- **Service Discovery**: Find available services for agent integration
- **Development Testing**: Identify test environments and services

### Security Considerations

- Network scanning should only be performed on networks you own or have permission to scan
- The discovery server uses safe, non-intrusive scanning methods
- All scanning activities are logged for audit purposes
- Consider firewall rules when deploying in production environments

## File Structure

```
/workspaces/adk_dev_trial/
├── mcp-config.json                 # Main MCP configuration
├── adk-python/                     # Google ADK Python source code
├── adk-docs/                       # Google ADK documentation
├── network_discovery_mcp/          # Custom network discovery server
│   ├── network_discovery_mcp/
│   │   ├── scanner.py              # Network scanning logic
│   │   └── server.py               # MCP server implementation
│   └── tests/                      # Test files
└── start-mcp-servers.sh           # Server startup script
```

## Troubleshooting

### Common Issues

1. **Network Discovery Not Working**:
   - Check if the network_discovery_mcp package is installed
   - Verify Python path and dependencies
   - Test basic functionality with `python test_basic.py`

2. **GitHub Server Authentication**:
   - Ensure GITHUB_TOKEN environment variable is set
   - Verify token has appropriate permissions
   - Check token expiration

3. **Filesystem Access Issues**:
   - Verify ALLOWED_DIRECTORIES includes correct paths
   - Check file permissions
   - Ensure repositories are cloned correctly

### Logging and Debugging

Enable verbose logging by setting:

```bash
export PYTHONPATH=/workspaces/adk_dev_trial/network_discovery_mcp:$PYTHONPATH
export MCP_DEBUG=1
```

## Next Steps

1. **Test Network Discovery**: Run network scans to verify functionality
2. **Integrate with ADK Agents**: Use discovered devices in agent workflows
3. **Extend Capabilities**: Add custom tools for specific device types
4. **Documentation**: Create device-specific interaction guides
5. **Security**: Implement authentication and access controls

## Support

For issues or questions:

- Check the ADK documentation in `/workspaces/adk_dev_trial/adk-docs/`
- Review network discovery tests in `network_discovery_mcp/tests/`
- Consult MCP protocol documentation for advanced configurations

---

*This setup provides a comprehensive foundation for ADK agent development with enhanced network discovery capabilities, enabling sophisticated device interaction and management scenarios.*
