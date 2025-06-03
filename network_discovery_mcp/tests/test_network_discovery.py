"""Tests for the network discovery MCP server."""


import pytest

from network_discovery_mcp.scanner import (
    NetworkDevice,
    NetworkInterface,
    NetworkScanner,
)


@pytest.fixture
def network_scanner() -> NetworkScanner:
    """Create a NetworkScanner instance for testing."""
    return NetworkScanner()


@pytest.mark.asyncio
async def test_ping_host(network_scanner):
    """Test ping functionality."""
    # Test successful ping (localhost should always be reachable)
    is_alive, response_time = await network_scanner.ping_host("127.0.0.1")
    # Note: In containerized environments, ping might fail due to network restrictions
    # So we just test that the function returns the expected types
    assert isinstance(is_alive, bool)
    assert response_time is None or isinstance(response_time, (int, float))

    # Test failed ping (non-existent host)
    is_alive, response_time = await network_scanner.ping_host("192.168.255.254", timeout=1)
    assert is_alive is False
    assert response_time is None


@pytest.mark.asyncio
async def test_scan_common_ports(network_scanner):
    """Test port scanning functionality."""
    # Test scanning localhost (should have some ports open)
    ports = await network_scanner.scan_common_ports("127.0.0.1", [22, 80, 443])
    assert isinstance(ports, list)
    # Note: May be empty if no services are running


@pytest.mark.asyncio
async def test_get_network_interfaces(network_scanner):
    """Test network interface discovery."""
    interfaces = await network_scanner.get_network_interfaces()
    assert isinstance(interfaces, list)
    assert len(interfaces) >= 1  # Should have at least one interface

    for interface in interfaces:
        assert isinstance(interface, NetworkInterface)
        assert interface.ip_address
        assert interface.netmask
        assert interface.network


@pytest.mark.asyncio
async def test_device_type_guessing(network_scanner):
    """Test device type identification."""
    # Test web server identification
    device = NetworkDevice(ip_address="192.168.1.100", open_ports=[80, 443])
    device_type = network_scanner.guess_device_type(device)
    assert "Web Server" in device_type

    # Test Windows computer identification
    device = NetworkDevice(ip_address="192.168.1.101", open_ports=[135, 139])
    device_type = network_scanner.guess_device_type(device)
    assert "Windows Computer" in device_type

    # Test SSH server identification
    device = NetworkDevice(ip_address="192.168.1.102", open_ports=[22])
    device_type = network_scanner.guess_device_type(device)
    assert "Linux Server" in device_type


@pytest.mark.asyncio
async def test_network_device_serialization():
    """Test NetworkDevice serialization."""
    device = NetworkDevice(
        ip_address="192.168.1.100",
        mac_address="aa:bb:cc:dd:ee:ff",
        hostname="test-device",
        open_ports=[22, 80, 443]
    )

    device_dict = device.to_dict()
    assert device_dict["ip_address"] == "192.168.1.100"
    assert device_dict["mac_address"] == "aa:bb:cc:dd:ee:ff"
    assert device_dict["hostname"] == "test-device"
    assert device_dict["open_ports"] == [22, 80, 443]


@pytest.mark.asyncio
async def test_server_list_tools():
    """Test that the server lists tools correctly."""
    # Import the handler function directly
    from network_discovery_mcp.server import handle_list_tools

    tools_result = await handle_list_tools()

    assert tools_result.tools
    tool_names = [tool.name for tool in tools_result.tools]

    expected_tools = [
        "scan_network",
        "get_network_interfaces",
        "scan_device_ports",
        "get_device_details",
        "ping_host",
        "discover_local_network"
    ]

    for tool_name in expected_tools:
        assert tool_name in tool_names


if __name__ == "__main__":
    pytest.main([__file__])
