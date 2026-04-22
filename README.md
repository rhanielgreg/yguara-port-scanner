A TCP port scanner built in Python with support for scanning IP ranges and user-defined port ranges. This tool is designed to quickly identify active services on a network, making it useful for infrastructure diagnostics, connectivity testing, and security assessments.

 Features
Scan multiple hosts using an IP range
Support for single ports or port ranges
Multi-threaded execution for improved performance
Detection of open ports
Configurable timeout to prevent hanging
Simple and straightforward CLI interface
Clean and organized output

 Usage

The user can input:

A single IP or a range of IPs (e.g., 192.168.0.1-192.168.0.254)
A single port or a range of ports (e.g., 80, 20-1000)

The tool scans the specified targets and returns the open ports found on each host.

 Technologies
Python 3
socket
concurrent.futures
threading


⚠️ Disclaimer

This tool is intended for use in authorized environments only. Unauthorized network scanning may violate laws and security policies.
