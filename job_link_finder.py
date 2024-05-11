from bs4 import BeautifulSoup
from urllib.parse import urljoin


def find_job_links(html_content, company_domain):
    soup = BeautifulSoup(html_content, 'html.parser')
    job_links = set()  # Use a set to deduplicate URLs

    # Find all occurrences of "product manager"
    product_manager_elements = soup.find_all(
        text=lambda text: "product manager" in text.lower())

    for element in product_manager_elements:
        # Find the parent element with an 'href' attribute
        parent = element.parent
        href = None
        while parent is not None and href is None:
            href = parent.get('href')
            if href is None:
                parent = parent.parent
            else:
                if href.startswith('/'):  # Check if the href is relative
                    href = urljoin(company_domain,
                                   href)  # Add company domain to relative link
                job_links.add(href)  # Add the href to the set
                break

    return job_links
