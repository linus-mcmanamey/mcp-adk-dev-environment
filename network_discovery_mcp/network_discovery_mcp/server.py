"""MCP Server for Network Discovery."""

import asyncio
import json
import logging
from typing import Any

from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsResult,
    TextContent,
    Tool,
)

from .scanner import NetworkScanner

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server
server: Server = Server("network-discovery")

# Initialize the network scanner
scanner = NetworkScanner()


@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List available network discovery tools."""
    return ListToolsResult(
        tools=[
            Tool(
                name="scan_network",
                description="Scan a network range for active devices",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "network": {
                            "type": "string",
                            "description": "Network range in CIDR notation (e.g., '192.168.1.0/24')",
                        },
                        "include_ports": {
                            "type": "boolean",
                            "description": "Whether to scan for open ports on discovered devices",
                            "default": False,
                        },
                    },
                    "required": ["network"],
                },
            ),
            Tool(
                name="get_network_interfaces",
                description="Get information about local network interfaces",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name="scan_device_ports",
                description="Scan specific ports on a target device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "host": {
                            "type": "string",
                            "description": "IP address or hostname of the target device",
                        },
                        "ports": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "List of ports to scan (if not provided, scans common ports)",
                        },
                    },
                    "required": ["host"],
                },
            ),
            Tool(
                name="get_device_details",
                description="Get detailed information about a specific device",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "ip_address": {
                            "type": "string",
                            "description": "IP address of the device to analyze",
                        },
                    },
                    "required": ["ip_address"],
                },
            ),
            Tool(
                name="ping_host",
                description="Ping a specific host to check if it's reachable",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "host": {
                            "type": "string",
                            "description": "IP address or hostname to ping",
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "Ping timeout in seconds",
                            "default": 1,
                        },
                    },
                    "required": ["host"],
                },
            ),
            Tool(
                name="discover_local_network",
                description="Automatically discover and scan the local network",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "include_ports": {
                            "type": "boolean",
                            "description": "Whether to scan for open ports on discovered devices",
                            "default": False,
                        },
                    },
                },
            ),
        ]
    )


@server.call_tool()
async def handle_call_tool(request: CallToolRequest) -> CallToolResult:
    """Handle tool execution requests."""
    try:
        arguments = request.params.arguments or {}

        if request.params.name == "scan_network":
            return await _scan_network(arguments)
        elif request.params.name == "get_network_interfaces":
            return await _get_network_interfaces(arguments)
        elif request.params.name == "scan_device_ports":
            return await _scan_device_ports(arguments)
        elif request.params.name == "get_device_details":
            return await _get_device_details(arguments)
        elif request.params.name == "ping_host":
            return await _ping_host(arguments)
        elif request.params.name == "discover_local_network":
            return await _discover_local_network(arguments)
        else:
            raise ValueError(f"Unknown tool: {request.params.name}")
    except Exception as e:
        logger.error(f"Error executing tool {request.params.name}: {e}")
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Error executing {request.params.name}: {str(e)}"
                )
            ]
        )


async def _scan_network(arguments: dict[str, Any]) -> CallToolResult:
    """Scan a network range for active devices."""
    network = arguments.get("network")
    include_ports = arguments.get("include_ports", False)

    if not network:
        raise ValueError("Network parameter is required")

    logger.info(f"Scanning network: {network}")
    devices = await scanner.scan_network_range(network, include_ports)

    # Format results
    results = []
    for device in devices:
        device_info = device.to_dict()
        device_info["device_type"] = scanner.guess_device_type(device)
        results.append(device_info)

    summary = f"Found {len(devices)} active devices on network {network}"

    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text=f"{summary}\n\nDevices:\n{json.dumps(results, indent=2)}"
            )
        ]
    )


async def _get_network_interfaces(arguments: dict[str, Any]) -> CallToolResult:
    """Get information about local network interfaces."""
    logger.info("Getting network interfaces")
    interfaces = await scanner.get_network_interfaces()

    results = [
        {
            "name": iface.name,
            "ip_address": iface.ip_address,
            "netmask": iface.netmask,
            "network": iface.network,
            "gateway": iface.gateway,
            "mac_address": iface.mac_address,
            "is_up": iface.is_up,
        }
        for iface in interfaces
    ]

    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text=f"Network Interfaces:\n{json.dumps(results, indent=2)}"
            )
        ]
    )


async def _scan_device_ports(arguments: dict[str, Any]) -> CallToolResult:
    """Scan specific ports on a target device."""
    host = arguments.get("host")
    ports = arguments.get("ports")

    if not host:
        raise ValueError("Host parameter is required")

    logger.info(f"Scanning ports on host: {host}")
    open_ports = await scanner.scan_common_ports(host, ports)

    services = {}
    if open_ports:
        services = await scanner.identify_device_services(host, open_ports)

    result = {
        "host": host,
        "open_ports": open_ports,
        "services": services,
        "total_open_ports": len(open_ports)
    }

    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text=f"Port scan results for {host}:\n{json.dumps(result, indent=2)}"
            )
        ]
    )


async def _get_device_details(arguments: dict[str, Any]) -> CallToolResult:
    """Get detailed information about a specific device."""
    ip_address = arguments.get("ip_address")

    if not ip_address:
        raise ValueError("IP address parameter is required")

    logger.info(f"Getting device details for: {ip_address}")
    device = await scanner.get_device_details(ip_address)

    if not device:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Device {ip_address} is not reachable or not found"
                )
            ]
        )

    device_info = device.to_dict()
    device_info["device_type"] = scanner.guess_device_type(device)

    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text=f"Device details for {ip_address}:\n{json.dumps(device_info, indent=2)}"
            )
        ]
    )


async def _ping_host(arguments: dict[str, Any]) -> CallToolResult:
    """Ping a specific host to check if it's reachable."""
    host = arguments.get("host")
    timeout = arguments.get("timeout", 1)

    if not host:
        raise ValueError("Host parameter is required")

    logger.info(f"Pinging host: {host}")
    is_alive, response_time = await scanner.ping_host(host, timeout)

    result = {
        "host": host,
        "is_reachable": is_alive,
        "response_time_ms": response_time * 1000 if response_time else None,
        "timeout": timeout
    }

    status = "reachable" if is_alive else "unreachable"

    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text=f"Ping result for {host}: {status}\n{json.dumps(result, indent=2)}"
            )
        ]
    )


async def _discover_local_network(arguments: dict[str, Any]) -> CallToolResult:
    """Automatically discover and scan the local network."""
    include_ports = arguments.get("include_ports", False)

    logger.info("Discovering local network")

    # Get network interfaces
    interfaces = await scanner.get_network_interfaces()

    if not interfaces:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text="No network interfaces found"
                )
            ]
        )

    all_devices = []
    scanned_networks = []

    # Scan each network
    for interface in interfaces:
        if interface.network and not interface.network.startswith("127."):
            logger.info(f"Scanning network: {interface.network}")
            devices = await scanner.scan_network_range(interface.network, include_ports)
            all_devices.extend(devices)
            scanned_networks.append(interface.network)

    # Format results
    device_results = []
    for device in all_devices:
        device_info = device.to_dict()
        device_info["device_type"] = scanner.guess_device_type(device)
        device_results.append(device_info)

    summary = {
        "scanned_networks": scanned_networks,
        "total_devices_found": len(all_devices),
        "devices": device_results
    }

    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text=f"Local network discovery complete:\n{json.dumps(summary, indent=2)}"
            )
        ]
    )


async def main():
    """Main entry point for the MCP server."""
    # Import here to avoid issues with imports
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="network-discovery",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
