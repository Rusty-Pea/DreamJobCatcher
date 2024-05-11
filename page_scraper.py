import requests
from bs4 import BeautifulSoup, Comment
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

    # Ask the user if they want to remove content outside the <body> tag
    remove_outside_body = input("Do you want to remove content outside the <body> tag? (y/n): ")
    if remove_outside_body.lower() == 'y':
        # Find the <body> tag
        body_tag = soup.body
        if body_tag:
            # Create a new BeautifulSoup object with only the <body> tag
            soup = BeautifulSoup(str(body_tag), 'html.parser')
        else:
            print("No <body> tag found in the HTML.")

    # Ask the user if they want to remove specific tags and comments
    remove_tags_comments = input("Do you want to remove <nav>, <header>, <footer>, <img>, <svg>, <canvas>, <noscript> tags, and HTML comments? (y/n): ")
    if remove_tags_comments.lower() == 'y':
        # Remove specified tags
        tags_to_remove = ['nav', 'header', 'footer', 'img', 'svg', 'canvas', 'noscript']
        for tag in tags_to_remove:
            for element in soup(tag):
                element.decompose()

        # Remove HTML comments
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

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