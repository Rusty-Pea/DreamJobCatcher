import subprocess
import json
import os
from job_link_finder import find_job_links
from datetime import datetime
from page_scraper import get_url_name
from page_scraper import scrape_url
from get_user_input import get_user_input
from search_linkedin import url_compiler
from search_linkedin import linkedin_company_url_retriever
from find_careers_sites_google import google_search_from_linkedin_urls
import job_page_change_detector
import mode_setting

# Perform the get_user_input function for search criteria - ASK THE USER STUFF
input_type_search_criteria = {
    "job role": "",
    "location": "",
    "industries": [],
    "keywords": [],
    "company size (minimum)": "",
    "company size (maximum)": ""
}

global mode
mode = input("Enter manually (m) or demo mode (d): ")

if mode == "d":
    mode_setting.get_demo_user()
    mode_setting.run_demo_user(input_type_search_criteria)
elif mode == "m":
    search_criteria = get_user_input(input_type_search_criteria)

print("End of asking user for input bit")

#####
# RUN LINKEDIN SEARCH TO FIND COMPANY PAGES ON LI
# TODO: this is hardcoded to allow file to run, needs removing
search_criteria = {
    'job role': 'product',
    'location': 'london',
    'industries': ['financial services'],
    'keywords': [''],
    'company size (minimum)': '5',
    'company size (maximum)': '500'
}

url_to_search = url_compiler(search_criteria)
#linkedin_company_url_retriever(url_to_search)   

print("End of LinkedIn searching bit")

##### CONVERT LINKEDIN PAGES TO CAREER PAGES WITH GOOGLE
# TODO: currently hardcoded urls - need to remove and take results from prior step
example_urls = [
    "https://www.linkedin.com/company/zegocover",
    "https://www.linkedin.com/company/finimize",
    "https://www.linkedin.com/company/prodigy-finance",
    "https://www.linkedin.com/company/clearscore",
    "https://www.linkedin.com/company/103785291/admin/inbox",
    "https://www.linkedin.com/company/entrepreneur-first",
    "https://www.linkedin.com/company/global-association-of-risk-professionals",
    "https://www.linkedin.com/company/yondercard",
    "https://www.linkedin.com/company/credit-benchmark",
    "https://www.linkedin.com/company/paymentsense",
    "https://www.linkedin.com/company/getmintago"
]

careers_urls = google_search_from_linkedin_urls(example_urls)

'''
print('Found the following urls:')
for careers_url in careers_urls:
    print(careers_url['search term'] + ': ' + careers_url['url'] )
'''

print("End of career page finding bit")

##### CHECK FOR PAGE CHANGES SINCE THE LAST CHECK
# Get career URLs
company_urls = [item['url'] for item in careers_urls]
company_domains = [url.split('/')[2] for url in company_urls]

# Check if 'outputs' folder exists, create if not
outputs_folder = 'outputs'
if not os.path.exists(outputs_folder):
    os.makedirs(outputs_folder)

# Get last checked file
last_checked_file = 'outputs/last_checked.json'
if os.path.isfile(last_checked_file):
    with open(last_checked_file, 'r') as file:
        last_checked_data = json.load(file)
else:
    last_checked_data = {}

# Check for changes
job_page_change_detector.check_for_changes(company_urls, last_checked_data, last_checked_file, search_criteria)
output_files = [f for f in os.listdir('outputs') if f.startswith('output_')]
if output_files:
    output_file = output_files[-1]  # Get the latest output file
else:
    print("No output file found.")
    exit()

# Read the JSON data about page changes
with open(f'outputs/{output_file}', 'r') as file:
    data = json.load(file)

print("End of page change checking bit")

#####
# Filter only URLs that had changes and have the target term
changed_urls = [
    url_data['URL'] for url_data in data
    if url_data['Change Detected?'] and url_data["Contains job role"]
]
print("End of change and role filtering bit")

#####
# Scrape all relevant URLs and get rid of irrelevant parts of the page
for url, domain in zip(changed_urls, company_domains):
    print(f"Scraping {url}")
    subprocess.run(["python", "page_scraper.py"],
                   input=f"{url}\ny\ny\n{domain}",
                   text=True)

print("End of career page scraping and removing pointless bits of html bit")


#####
# Find job links in the scraped content
job_links = []
for filename in os.listdir('outputs'):
    if filename.startswith("ps_"):
        file_path = os.path.join('outputs', filename)
        with open(file_path, 'r') as file:
            html_content = file.read()

        company_domains_copy = company_domains.copy()  # Create a new copy for each iteration
        found_job_links = find_job_links(html_content, company_domains_copy.pop(0))
        for link in found_job_links:
            job_links.append({"job_url": link, "assessment": ""})

# Write job links to a JSON file
with open('outputs/job_list.json', 'w') as file:
    json.dump(job_links, file, indent=2)

print("Job links saved to outputs/job_list.json")
print("End of job link finding bit")

#####
# Create the 'job_files' folder if it doesn't exist
job_files_folder = os.path.join('outputs', 'job_files')
if not os.path.exists(job_files_folder):
    os.makedirs(job_files_folder)

# Scrape each job link and save the content to a separate file
with open('outputs/job_list.json', 'r') as file:
    job_links = json.load(file)

for job_data in job_links:
    job_link = job_data['job_url']
    job_filename = f"{get_url_name(job_link)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    job_file_path = os.path.join(job_files_folder, job_filename)

    # Call the scrape_url function from page_scraper.py
    output_file = scrape_url(job_link,
                             remove_outside_body=True,
                             remove_tags_comments=True)

    if output_file:
        # Move the output file to the job_files folder
        os.rename(output_file, job_file_path)
        print(f"Job content saved to {job_file_path}")

print("End of job link scraping bit")

#####
# TODO: CREATE LIST OF JOBS

#####
# TODO: ANALYSE JOBS

print("Full run completed")