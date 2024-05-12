from bs4 import BeautifulSoup
from urllib.parse import urljoin

#TODO: Relative href bit still doesnt work

def find_job_links(html_content, company_domain, search_criteria):
    soup = BeautifulSoup(html_content, 'html.parser')
    job_links = set()  # Use a set to deduplicate URLs

    # Find all occurrences of job role
    job_role_elements = soup.find_all(text=lambda text: search_criteria['job_role'] in text.lower())

    if len(job_role_elements) == 0:
        job_links.add("No role mentions found")
    else:

        for element in job_role_elements:
            # Find the parent element with an 'href' attribute
            parent = element.parent
            href = None
            while parent is not None and href is None:
                href = parent.get('href')
                if href is None:
                    parent = parent.parent
                    print("Went up href parent")
                else:
                    if not href.startswith('http'):  # Check if the href is relative
                        href = urljoin(company_domain, href)  # Add company domain to relative link
                    job_links.add(href)  # Add the href to the set
                    break

            if href is None:
                job_links.add("No href found")

    return job_links