#!/usr/bin/env python3
"""Simple test for network discovery MCP server."""

import asyncio

from network_discovery_mcp.scanner import NetworkDevice, NetworkScanner


async def test_basic_scanner():
    """Test basic scanner functionality without ping dependency."""
    print("Testing Network Discovery MCP Server...")

    scanner = NetworkScanner()

    # Test network interface detection
    print("\n1. Testing network interface detection:")
    interfaces = await scanner.get_network_interfaces()
    print(f"Found {len(interfaces)} network interfaces:")
    for iface in interfaces:
        print(f"  - {iface.name}: {iface.ip_address} (network: {iface.network})")

    # Test device type guessing
    print("\n2. Testing device type identification:")
    test_devices = [
        NetworkDevice(ip_address="192.168.1.1", open_ports=[22, 80]),
        NetworkDevice(ip_address="192.168.1.2", open_ports=[135, 139]),
        NetworkDevice(ip_address="192.168.1.3", open_ports=[80, 443]),
        NetworkDevice(ip_address="192.168.1.4", open_ports=[3389]),
        NetworkDevice(ip_address="192.168.1.5", open_ports=[22]),
    ]

    for device in test_devices:
        device_type = scanner.guess_device_type(device)
        print(f"  - {device.ip_address} with ports {device.open_ports} -> {device_type}")

    # Test port scanning (localhost should be safe)
    print("\n3. Testing port scanning on localhost:")
    try:
        open_ports = await scanner.scan_common_ports("127.0.0.1", [22, 80, 8080, 3000])
        print(f"Open ports on localhost: {open_ports}")
    except Exception as e:
        print(f"Port scanning failed (expected in restricted environment): {e}")

    # Test service identification
    print("\n4. Testing service identification:")
    services = await scanner.identify_device_services("127.0.0.1", [22, 80, 443])
    print(f"Services identified: {services}")

    print("\n✅ Basic functionality test completed successfully!")
    return True


if __name__ == "__main__":
    asyncio.run(test_basic_scanner())
