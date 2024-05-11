import subprocess
import json
import os
from job_link_finder import find_job_links  # Import the find_job_links function

# Run job_page_change_detector.py and get the output file
subprocess.run(["python", "job_page_change_detector.py"])

# Get the name of the output file
output_files = [f for f in os.listdir('.') if f.startswith('output_')]
if output_files:
    output_file = output_files[-1]  # Get the latest output file
else:
    print("No output file found.")
    exit()

# Read the JSON data from the output file
with open(output_file, 'r') as file:
    data = json.load(file)

# Filter out the URLs that had no changes
changed_urls = [url_data['URL'] for url_data in data if url_data['Change Detected?'] and url_data['Contains \'product manager\'']]

# Run page_scraper.py for each changed URL with both options set to 'y'
for url in changed_urls:
    print(f"Scraping {url}")
    subprocess.run(["python", "page_scraper.py"], input=f"{url}\ny\ny", text=True)

# Find job links in the output files from page_scraper.py
job_links_file = open('job_list.txt', 'w')
for filename in os.listdir('.'):
    if filename.startswith("ps_"):
        file_path = os.path.join('.', filename)
        with open(file_path, 'r') as file:
            html_content = file.read()

        job_links = find_job_links(html_content)
        for link in job_links:
            job_links_file.write(link + '\n')

job_links_file.close()
print("Job links saved to job_list.txt")

print("Scraping and job link finding completed.")