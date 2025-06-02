# Network Discovery MCP Server

A Model Context Protocol (MCP) server for discovering and identifying devices on your local area network.

## Features

- **Network Scanning**: Discover active devices on your local network
- **Device Identification**: Identify device types, operating systems, and services
- **Port Scanning**: Detect open ports and running services
- **Network Interface Discovery**: Enumerate local network interfaces
- **DHCP Client Detection**: Identify DHCP-assigned devices
- **Network Topology Mapping**: Create a map of your network structure

## Installation

```bash
cd network_discovery_mcp
pip install -e .
```

## Usage

### As MCP Server

Add to your MCP configuration:

```json
{
  "servers": {
    "network-discovery": {
      "command": "python",
      "args": ["-m", "network_discovery_mcp.server"],
      "env": {}
    }
  }
}
```

### Available Tools

- `scan_network`: Scan a network range for active devices
- `identify_device`: Get detailed information about a specific device
- `scan_ports`: Scan ports on a specific host
- `get_network_interfaces`: List local network interfaces
- `get_network_topology`: Generate network topology map
- `discover_services`: Discover services running on network devices

## Security Note

This tool performs network scanning which may trigger security alerts. Use only on networks you own or have explicit permission to scan.

## Requirements

- Python 3.10+
- nmap (system package)
- Administrative privileges may be required for some scanning features

## License

MIT License
