"""Network scanning and device discovery utilities."""

import asyncio
import ipaddress
import logging
import socket
import time
from dataclasses import asdict, dataclass
from typing import Any

# Note: nmap python library requires system nmap package
# We'll use basic socket and subprocess methods instead
nmap = None

try:
    import netifaces  # type: ignore
except ImportError:
    netifaces = None

try:
    from scapy.all import ARP, Ether, srp  # type: ignore
    scapy_available = True
except ImportError:
    ARP = None
    Ether = None
    srp = None
    scapy_available = False

logger = logging.getLogger(__name__)


@dataclass
class NetworkDevice:
    """Represents a discovered network device."""
    ip_address: str
    mac_address: str | None = None
    hostname: str | None = None
    vendor: str | None = None
    os_guess: str | None = None
    open_ports: list[int] | None = None
    services: dict[int, str] | None = None
    device_type: str | None = None
    last_seen: float | None = None
    response_time: float | None = None

    def __post_init__(self) -> None:
        if self.open_ports is None:
            self.open_ports = []
        if self.services is None:
            self.services = {}
        if self.last_seen is None:
            self.last_seen = time.time()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class NetworkInterface:
    """Represents a network interface."""
    name: str
    ip_address: str
    netmask: str
    network: str
    gateway: str | None = None
    mac_address: str | None = None
    is_up: bool = True


class NetworkScanner:
    """Network scanner for device discovery."""

    def __init__(self) -> None:
        self.devices: dict[str, NetworkDevice] = {}

    async def get_network_interfaces(self) -> list[NetworkInterface]:
        """Get all network interfaces on the local machine."""
        interfaces = []

        if netifaces is None:
            logger.warning("netifaces not available, using basic interface detection")
            return await self._get_interfaces_basic()

        try:
            for interface_name in netifaces.interfaces():
                interface_info = netifaces.ifaddresses(interface_name)

                # Get IPv4 addresses
                if netifaces.AF_INET in interface_info:
                    for addr_info in interface_info[netifaces.AF_INET]:
                        ip_addr = addr_info.get('addr')
                        netmask = addr_info.get('netmask')

                        if ip_addr and netmask and not ip_addr.startswith('127.'):
                            # Calculate network
                            network = ipaddress.IPv4Network(f"{ip_addr}/{netmask}", strict=False)

                            # Get MAC address
                            mac_addr = None
                            if netifaces.AF_LINK in interface_info:
                                mac_addr = interface_info[netifaces.AF_LINK][0].get('addr')

                            # Get gateway
                            gateway = None
                            gateways = netifaces.gateways()
                            if 'default' in gateways and netifaces.AF_INET in gateways['default']:
                                gateway = gateways['default'][netifaces.AF_INET][0]

                            interfaces.append(NetworkInterface(
                                name=interface_name,
                                ip_address=ip_addr,
                                netmask=netmask,
                                network=str(network.network_address) + "/" + str(network.prefixlen),
                                gateway=gateway,
                                mac_address=mac_addr
                            ))
        except Exception as e:
            logger.error(f"Error getting network interfaces: {e}")
            return await self._get_interfaces_basic()

        return interfaces

    async def _get_interfaces_basic(self) -> list[NetworkInterface]:
        """Basic interface detection using socket."""
        try:
            # Get the local IP address by connecting to a remote address
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()

            # Assume /24 network
            network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)

            return [NetworkInterface(
                name="default",
                ip_address=local_ip,
                netmask="255.255.255.0",
                network=str(network.network_address) + "/24"
            )]
        except Exception as e:
            logger.error(f"Error with basic interface detection: {e}")
            return []

    async def ping_host(self, host: str, timeout: int = 1) -> tuple[bool, float | None]:
        """Ping a host to check if it's alive."""
        try:
            start_time = time.time()

            # Use system ping command
            process = await asyncio.create_subprocess_exec(
                'ping', '-c', '1', '-W', str(timeout), host,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )

            returncode = await process.wait()
            response_time = time.time() - start_time

            return returncode == 0, response_time if returncode == 0 else None

        except Exception as e:
            logger.debug(f"Ping failed for {host}: {e}")
            return False, None

    async def scan_network_range(self, network: str, include_ports: bool = False) -> list[NetworkDevice]:
        """Scan a network range for active devices."""
        try:
            net = ipaddress.IPv4Network(network, strict=False)
        except ValueError as e:
            logger.error(f"Invalid network range: {network}: {e}")
            return []

        devices = []
        tasks = []

        # Create ping tasks for all hosts in the network
        for host in net.hosts():
            if net.num_addresses > 256:  # Limit scan size for large networks
                break
            tasks.append(self._scan_single_host(str(host), include_ports))

        # Execute all ping tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, NetworkDevice):
                devices.append(result)
                self.devices[result.ip_address] = result

        return devices

    async def _scan_single_host(self, host: str, include_ports: bool = False) -> NetworkDevice | None:
        """Scan a single host."""
        is_alive, response_time = await self.ping_host(host)

        if not is_alive:
            return None

        device = NetworkDevice(ip_address=host, response_time=response_time)

        # Try to get hostname
        try:
            hostname = socket.gethostbyaddr(host)[0]
            device.hostname = hostname
        except (socket.herror, socket.gaierror, OSError):
            pass

        # Get MAC address using ARP (if scapy is available)
        if scapy_available and ARP and Ether and srp:
            try:
                arp_request = ARP(pdst=host)
                broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
                arp_request_broadcast = broadcast / arp_request
                answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

                if answered_list:
                    device.mac_address = answered_list[0][1].hwsrc
            except Exception as e:
                logger.debug(f"ARP scan failed for {host}: {e}")

        # Port scanning if requested
        if include_ports:
            device.open_ports = await self.scan_common_ports(host)

        return device

    async def scan_common_ports(self, host: str, ports: list[int] | None = None) -> list[int]:
        """Scan common ports on a host."""
        if ports is None:
            # Common ports to scan
            ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 1723, 3389, 5900]

        open_ports = []
        semaphore = asyncio.Semaphore(10)  # Limit concurrent connections

        async def scan_port(port: int) -> int | None:
            async with semaphore:
                try:
                    future = asyncio.open_connection(host, port)
                    reader, writer = await asyncio.wait_for(future, timeout=1.0)
                    writer.close()
                    await writer.wait_closed()
                    return port
                except (asyncio.TimeoutError, OSError, ConnectionRefusedError):
                    return None

        tasks = [scan_port(port) for port in ports]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, int):
                open_ports.append(result)

        return sorted(open_ports)

    async def identify_device_services(self, host: str, ports: list[int]) -> dict[int, str]:
        """Identify services running on specific ports."""
        services = {}

        service_map = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            111: "RPC",
            135: "MS RPC",
            139: "NetBIOS",
            143: "IMAP",
            443: "HTTPS",
            993: "IMAPS",
            995: "POP3S",
            1723: "PPTP",
            3389: "RDP",
            5900: "VNC"
        }

        for port in ports:
            if port in service_map:
                services[port] = service_map[port]
            else:
                # Try to identify service by banner grabbing
                try:
                    reader, writer = await asyncio.wait_for(
                        asyncio.open_connection(host, port), timeout=2.0
                    )

                    # Read banner
                    banner = await asyncio.wait_for(reader.read(100), timeout=1.0)
                    writer.close()
                    await writer.wait_closed()

                    banner_str = banner.decode('utf-8', errors='ignore').strip()
                    if banner_str:
                        services[port] = f"Unknown ({banner_str[:30]})"
                    else:
                        services[port] = "Unknown"

                except (asyncio.TimeoutError, OSError, ConnectionRefusedError, UnicodeDecodeError):
                    services[port] = "Unknown"

        return services

    async def get_device_details(self, ip_address: str) -> NetworkDevice | None:
        """Get detailed information about a specific device."""
        device: NetworkDevice | None = None

        if ip_address in self.devices:
            device = self.devices[ip_address]
        else:
            device = await self._scan_single_host(ip_address, include_ports=True)
            if device:
                self.devices[ip_address] = device

        if device and device.open_ports:
            device.services = await self.identify_device_services(ip_address, device.open_ports)

        return device

    def guess_device_type(self, device: NetworkDevice) -> str:
        """Guess device type based on open ports and services."""
        if not device.open_ports:
            return "Unknown"

        ports = set(device.open_ports)

        # Web server
        if 80 in ports or 443 in ports:
            if 22 in ports:
                return "Web Server (Linux)"
            elif 3389 in ports:
                return "Web Server (Windows)"
            else:
                return "Web Server"

        # Router/Gateway
        if 23 in ports or (80 in ports and 53 in ports):
            return "Router/Gateway"

        # Network printer
        if 631 in ports or 9100 in ports:
            return "Network Printer"

        # Windows machine
        if 135 in ports and 139 in ports:
            return "Windows Computer"

        # SSH server (likely Linux)
        if 22 in ports and 80 not in ports:
            return "Linux Server"

        # RDP server
        if 3389 in ports:
            return "Windows Desktop/Server"

        # VNC server
        if 5900 in ports:
            return "VNC Server"

        return "Unknown Device"
