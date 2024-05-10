import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
import subprocess

def check_for_changes(urls, last_checked_file):
    # Load last checked data from the JSON file
    try:
        with open(last_checked_file, 'r') as file:
            last_checked_data = json.load(file)
    except FileNotFoundError:
        last_checked_data = {}

    # Lists to store output
    changed_data = []
    unchanged_data = []

    # Iterate over URLs
    for i, url in enumerate(urls, start=1):
        try:
            # Get URL contents, parse with BS, convert soup to string
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            current_content = str(soup)

            # Get the last checked content for this URL
            last_checked_content = last_checked_data.get(url)

            # Compare current content with last checked content
            if last_checked_content is None or current_content != last_checked_content:
                change_detected = True
                # Check for product manager in latest content
                contains_product_manager = "product manager" in current_content.lower()
                # Update the last checked content for the URL
                last_checked_data[url] = current_content
            else:
                change_detected = False
                contains_product_manager = False

            # Create a dictionary for the current URL's output
            url_output = {
                "URL": url,
                "Change Detected?": change_detected,
                "Contains 'product manager'": contains_product_manager,
            }

            # Append the URL's output to the appropriate list based on change detection
            if change_detected:
                changed_data.append(url_output)
            else:
                unchanged_data.append(url_output)

        except requests.exceptions.RequestException as e:
            print(f"\nError checking {url}: {e}")

    print("\nCheck completed.")

urls = [
    'https://healthy.io/eu/careers/',
    'https://www.livi.co.uk/careers/business/',
    'https://apply.workable.com/elvie/',
]
last_checked_file = 'last_checked.json'

check_for_changes(urls, last_checked_file)