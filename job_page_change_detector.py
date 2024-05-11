import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
import subprocess
import os

# Check if 'outputs' folder exists, create if not
outputs_folder = 'outputs'
if not os.path.exists(outputs_folder):
    os.makedirs(outputs_folder)

# Read URLs from the JSON file
with open('company_urls.json', 'r') as file:
    urls = json.load(file)

last_checked_file = 'outputs/last_checked.json'  # Update file path

if os.path.isfile(last_checked_file):
    with open(last_checked_file, 'r') as file:
        last_checked_data = json.load(file)
else:
    last_checked_data = {}


def check_for_changes(urls, last_checked_data):
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
                contains_product_manager = "product manager" in current_content.lower(
                )
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

            # CL progress indicator
            progress = f"[{'=' * (i - 1)}{' ' * (len(urls) - i)}]"
            print(f"\rChecking URLs... {progress} {i}/{len(urls)}",
                  end="",
                  flush=True)

        except requests.exceptions.RequestException as e:
            print(f"\nError checking {url}: {e}")

        # Add a delay so we don't get blocked
        time.sleep(1)

    print("\nCheck completed.")

    # Sort by presence of "product manager"
    changed_data.sort(key=lambda x: (not x["Contains 'product manager'"]))

    # Combine changed and unchanged data
    output_data = changed_data + unchanged_data

    # Save updated last checked data to JSON file
    with open(last_checked_file, 'w') as file:
        json.dump(last_checked_data, file, indent=4)

    # Generate output file name with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"outputs/output_{timestamp}.json"

    # Save the output data to JSON file
    with open(output_file, 'w') as file:
        json.dump(output_data, file, indent=4)


check_for_changes(urls, last_checked_data)
