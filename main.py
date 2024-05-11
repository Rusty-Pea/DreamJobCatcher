import subprocess
import json
import os
from job_link_finder import find_job_links
from datetime import datetime
from page_scraper import get_url_name
from page_scraper import scrape_url

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

        company_domains_copy = company_domains.copy()  # Create a new copy for each iteration
        job_links = find_job_links(html_content, company_domains_copy.pop(0))
        for link in job_links:
            job_links_file.write(link + '\n')

job_links_file.close()
print("Job links saved to outputs/job_list.txt")

# Create the 'job_files' folder if it doesn't exist
job_files_folder = os.path.join('outputs', 'job_files')
if not os.path.exists(job_files_folder):
    os.makedirs(job_files_folder)

# Scrape each job link and save the content to a separate file
with open('outputs/job_list.txt', 'r') as file:
    job_links = file.readlines()

for job_link in job_links:
    job_link = job_link.strip()  # Remove any leading/trailing whitespace
    job_filename = f"{get_url_name(job_link)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    job_file_path = os.path.join(job_files_folder, job_filename)

    # Call the scrape_url function from page_scraper.py
    output_file = scrape_url(job_link, remove_outside_body=True, remove_tags_comments=True)

    if output_file:
        # Move the output file to the job_files folder
        os.rename(output_file, job_file_path)
        print(f"Job content saved to {job_file_path}")

print("Scraping and job content saving completed.")