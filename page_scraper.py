import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def get_url_name(url):
    # Remove the protocol (http:// or https://)
    url_name = re.sub(r'^https?://', '', url)
    # Replace non-alphanumeric characters with underscores
    url_name = re.sub(r'[^a-zA-Z0-9]', '_', url_name)
    return url_name

# Prompt the user for a URL
url = input("Enter a URL: ")

try:
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Generate the file name using the URL's name and timestamp
    url_name = get_url_name(url)
    file_name = f"{url_name}_{timestamp}.txt"

    # Write the BeautifulSoup output to the file
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f"BeautifulSoup output saved to {file_name}")

except requests.exceptions.RequestException as e:
    print(f"Error accessing the URL: {e}")