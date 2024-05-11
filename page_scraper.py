import requests
from bs4 import BeautifulSoup, Comment
from datetime import datetime
import re
import os

def get_url_name(url):
    # Remove the protocol (http:// or https://)
    url_name = re.sub(r'^https?://', '', url)
    # Replace non-alphanumeric characters with underscores
    url_name = re.sub(r'[^a-zA-Z0-9]', '_', url_name)
    return url_name

def scrape_url(url, remove_outside_body=False, remove_tags_comments=False):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        if remove_outside_body:
            # Remove content outside the <body> tag
            body_tag = soup.body
            if body_tag:
                soup = BeautifulSoup(str(body_tag), 'html.parser')
            else:
                print("No <body> tag found in the HTML.")

        if remove_tags_comments:
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
        file_name = f"{outputs_folder}/ps_{url_name}_{timestamp}.txt"

        # Write the BeautifulSoup output to the file
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(str(soup))

        return file_name

    except requests.exceptions.RequestException as e:
        print(f"Error accessing the URL: {e}")
        return None

# Create "outputs" folder if it doesn't exist
outputs_folder = 'outputs'
if not os.path.exists(outputs_folder):
    os.makedirs(outputs_folder)

if __name__ == "__main__":
    # Prompt the user for a URL
    url = input("Enter a URL: ")

    remove_outside_body = input("Do you want to remove content outside the <body> tag? (y/n): ")
    remove_outside_body = remove_outside_body.lower() == 'y'

    remove_tags_comments = input("Do you want to remove <nav>, <header>, <footer>, <img>, <svg>, <canvas>, <noscript> tags, and HTML comments? (y/n): ")
    remove_tags_comments = remove_tags_comments.lower() == 'y'

    file_name = scrape_url(url, remove_outside_body, remove_tags_comments)

    if file_name:
        print(f"BeautifulSoup output saved to {file_name}")