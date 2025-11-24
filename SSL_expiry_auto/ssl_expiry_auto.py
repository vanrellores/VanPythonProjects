import json
import requests
import ssl
import socket
from datetime import datetime

def get_ssl_expiry(domain):
    port = 443  # default HTTPS port

    # Create SSL context
    context = ssl.create_default_context()

    # Create TCP connection, wrap it with SSL
    with socket.create_connection((domain, port)) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()

    # Extract expiry date
    expiry_str = cert['notAfter']  # e.g., 'Nov  7 23:59:59 2025 GMT'
    expiry_date = datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z")

    return expiry_date

# Example usage
domain = input(str("Enter domain: "))
expiry_date = get_ssl_expiry(domain)
print(f"{domain} SSL certificate expires on: {expiry_date}")

