import requests
from urllib3.exceptions import InsecureRequestWarning
import json

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def test_encryption():
    # Base URLs for HTTP and HTTPS
    http_url = 'http://localhost:5001/sensitive-data'
    https_url = 'https://localhost:5001/sensitive-data'
    
    print("Testing HTTP vs HTTPS connections:\n")
    
    # Try HTTP request (should be redirected to HTTPS)
    try:
        response = requests.get(http_url, allow_redirects=False)
        print(f"HTTP Request:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {json.dumps(dict(response.headers), indent=2)}")
        print("(Should see a redirect to HTTPS)\n")
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}\n")
    
    # Try HTTPS request
    try:
        response = requests.get(https_url, verify=False)  # verify=False for self-signed cert
        print(f"HTTPS Request:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {json.dumps(dict(response.headers), indent=2)}")
        print(f"Data: {json.dumps(response.json(), indent=2)}\n")
    except requests.exceptions.RequestException as e:
        print(f"HTTPS Request failed: {e}\n")
    
    # Show security headers
    if response.status_code == 200:
        print("Security Headers:")
        for header, value in response.headers.items():
            if header.lower().startswith(('strict-transport', 'content-security')):
                print(f"{header}: {value}")

if __name__ == "__main__":
    test_encryption() 