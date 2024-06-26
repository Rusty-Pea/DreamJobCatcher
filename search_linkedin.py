from selenium import webdriver
from selenium.webdriver.common.by import By
import json


# compile search for url
def url_compiler(search_criteria):
    # LOCATION
    # lookup for named locations to codes for LinkedIn purposes
    location_library = {
        "london": '90009496',
        "uk": '101165590',
        "san francisco": '90000084',
        "madrid": '100994331'
    }

    # location formatted
    # defaults to london if not found
    location_code = location_library.get(search_criteria['location'], location_library["london"])

    # INDUSTRIES

    # lookup for industries locations to codes for LinkedIn purposes

    lookup_linkedin_industries = 'lookup_linkedin_industries.json'
    with open(lookup_linkedin_industries, 'r') as file:
        industries = json.load(file)["industries"]
        print(industries)
    print(search_criteria['industries'])
    industries_ids = []
    for industry in industries:
        for search_criteria_industry in search_criteria['industries']:
            if industry["name"].lower() == search_criteria_industry.lower():
                industries_ids.append(str(industry["id"]))

    industries_code = '%5B%22' + '%22%2C%22'.join(industries_ids) + '%22%5D'

    # uncomment to hardcode
    # industries_code = '%5B%2243%22%5D'


    # TODO: ignoring keywords for now
    # list of keywords concat into string with %20
    # keywords_for_url_search = '%20'.join(search_criteria['keywords']).replace(
    #     ' ', '')


    # company size
    # TODO: this is not quite correct but illustrative

    company_size_library = {
        0: 'A',
        10: 'B',
        50: 'C',
        200: 'D',
        500: 'E',
        1000: 'F',
        5000: 'G',
        10000: 'H',
        999999: 'I'
    }

    categories = []

    for size, category in company_size_library.items():
        min_range = int(search_criteria['company size (minimum)'])
        max_range = int(search_criteria['company size (maximum)'])

        if min_range <= size <= max_range:
            categories.append(category)
    # print(categories)

    company_size_for_url = '%5B%22' + '%22%2C%22'.join(categories) + '%22%5D'
    # print(company_size_for_url)



    # linked url ends with this format, but seems to not be needed
    # &sid=%3BHH

    # with keywords
    # linkedin_search_url = f"https://www.linkedin.com/search/results/COMPANIES/?companyHqGeo=%5B%22{location_code}%22%5D&companySize={company_size_for_url}&industryCompanyVertical={industries_code}&keywords='{keywords_for_url_search}'&origin=FACETED_SEARCH"

    # without keywords
    linkedin_search_url = f"https://www.linkedin.com/search/results/COMPANIES/?companyHqGeo=%5B%22{location_code}%22%5D&companySize={company_size_for_url}&industryCompanyVertical={industries_code}&origin=FACETED_SEARCH"

    print(linkedin_search_url)
    return linkedin_search_url

    # TODO: work through pagination
    # append &page=1 for pagination


def linkedin_company_url_retriever(linkedin_search_url):
    # Initialize the driver (e.g., for Chrome)
    driver = webdriver.Chrome()

    # Navigate to the webpage
    driver.get(linkedin_search_url)

    input("Opened web page. Log in if needed. Press enter when done.")

    # get relevant elements from page
    link_elements = driver.find_elements(By.CLASS_NAME, "app-aware-link")

    # take the urls from these
    link_elements_urls = [
        link_element.get_attribute('href') for link_element in link_elements
    ]

    # filter for only company urls
    prefix = 'https://www.linkedin.com/company/'
    links_linkedin_companies = list(
        set(list(filter(lambda x: x.startswith(prefix), link_elements_urls))))
    print(str(len(links_linkedin_companies)) + ' companies found')
    print(*links_linkedin_companies, sep='\n')

    return links_linkedin_companies
