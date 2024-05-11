import subprocess
import json
import os
from job_link_finder import find_job_links  # Import the find_job_links function

# Read company domains from the JSON file
company_urls_file = 'company_urls.json'
with open(company_urls_file, 'r') as file:
    company_urls = json.load(file)
    company_domains = [url.split('/')[2] for url in company_urls]

# Check for page changes since the last time it ran
subprocess.run(["python", "job_page_change_detector.py"])
output_files = [f for f in os.listdir('outputs') if f.startswith('output_')]
if output_files:
    output_file = output_files[-1]  # Get the latest output file
else:
    print("No output file found.")
    exit()

# Read the JSON data about page changes
with open(f'outputs/{output_file}', 'r') as file:
    data = json.load(file)

# Filter only URLs that had changes and have the target term
changed_urls = [
    url_data['URL'] for url_data in data
    if url_data['Change Detected?'] and url_data["Contains 'product manager'"]
]

# Scrape all relevant URLs and get rid of irrelevant parts of the page
for url, domain in zip(changed_urls, company_domains):
    print(f"Scraping {url}")
    subprocess.run(["python", "page_scraper.py"],
                   input=f"{url}\ny\ny\n{domain}",
                   text=True)

# Find job links in the scraped content
job_links_file = open('outputs/job_list.txt', 'w')
for filename in os.listdir('outputs'):
    if filename.startswith("ps_"):
        file_path = os.path.join('outputs', filename)
        with open(file_path, 'r') as file:
            html_content = file.read()

        job_links = find_job_links(html_content, company_domains.pop(0))
        for link in job_links:
            job_links_file.write(link + '\n')

job_links_file.close()
print("Job links saved to outputs/job_list.txt")
print("Scraping and job link finding completed.")
