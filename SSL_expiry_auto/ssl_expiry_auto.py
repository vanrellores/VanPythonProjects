import requests
import json
import ssl
import socket
from datetime import datetime
from requests.auth import HTTPBasicAuth

zendesk_ticket_id = input("Enter Zendesk Ticket ID: ")
url = f"https://cloudservices-support.zendesk.com/api/v2/tickets/{zendesk_ticket_id}"
headers = {
	"Content-Type": "application/json",
}
email_address = input("Enter your Zendesk email address: ")
api_token = input("Enter your Zendesk API token: ")
# Use basic authentication
auth = HTTPBasicAuth(f'{email_address}/token', api_token)

"""
response = requests.request(
	"GET",
	url,
	auth=auth,
	headers=headers
)
"""

response = requests.get(
	url,
	auth=auth,
	headers=headers
)

def get_domain():
	data = response.json()

	ticket_description = data["ticket"]["description"]

	host_value = None

	for line in ticket_description.splitlines():
		if line.startswith("Host:"):
			host_value = line.split("Host:")[1].strip()
			break
	return host_value

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

    now = datetime.now()
    print(now)

    days_remaining = (expiry_date - now).days
    return days_remaining, expiry_date

# Example usage

domain = get_domain()
days_remaining, expiry_date = get_ssl_expiry(domain)

if days_remaining <= 30:
    print(f"{domain}'s SSL certificate expires on {expiry_date} in {days_remaining} days. \nPlease advise requester to renew the SSL certificate.")
else:
    print(f"{domain}'s SSL certificate expires on {expiry_date} in {days_remaining} days. \nClose the ticket.")

