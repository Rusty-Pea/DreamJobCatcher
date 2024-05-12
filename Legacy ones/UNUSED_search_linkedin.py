
import requests
from bs4 import BeautifulSoup
#
# linkedin_companies_results = """
# <a class="app-aware-link " href="https://www.linkedin.com/company/mutusystem/" data-test-app-aware-link=""> MUTU System</a>
# """
#
#
# # Extract and print the href attributes
# for link in links:
#     href = link.get('href')
#     if href:  # Ensure the href exists before printing
#         print(f'href="{href}"')


# METHOD 1

# TODO: need to log in or find method through API
# def get_url_name_linkedin_companies(url):
#     try:
#         # Send a GET request to the URL
#         # response = requests.get(url)
#         response = requests.get(url, auth=('aidangoodall7@gmail.com', 'jD8Kih5X'))
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         # Parse the HTML content using BeautifulSoup
#         # soup = BeautifulSoup(response.text, 'html.parser')
#
#         # print(type(soup))
#         print(soup)
#         # Find all elements with the class "app-aware-link"
#         # filter for specific links containing "company" format
#         prefix = 'https://www.linkedin.com/company/'
#
#         links = soup.find_all('a', class_='app-aware-link')
#         print(links)
#         # links_linkedin_companies = []
#         #
#         # for link in links:
#         #     if link.startswith(prefix):
#         #         links_linkedin_companies.append({"name": link, "url": link})
#         #
#         # return links_linkedin_companies
#         return links
#
#     except requests.exceptions.RequestException as e:
#         print(f"Error accessing the URL: {e}")
#
#
#
#
#
#
#
# # Example usage
# url_list = [
#     "https://www.google.com",
#     "https://www.linkedin.com/company/acme-inc",
#     "http://example.com",
#     "https://www.linkedin.com/company/stark-industries",
#     "https://www.facebook.com"
# ]
#
# # result =
# get_url_name_linkedin_companies(linkedin_search_url)
# print(result)


#
#
# # METHOD 2
#
# # go to url
#
# webbrowser.get('safari').open(linkedin_search_url)  # Go to example.com
#
# # Wait for the user to interact with the search page
# input("Opened web page. Log in if needed. Open interesting looking companies in a new tab within the same browser. Press enter when done.")
#
# # Get the list of currently opened tabs
# tabs = webbrowser.get().tabs()
#
# # Open each tab in a new tab
# for tab in tabs:
#     # Get the URL of the current tab
#     url = tab.url
#
#     # Check if the URL is a LinkedIn company page
#     if "linkedin.com/company/" in url:
#         # Open the company page in a new tab
#         webbrowser.open_new_tab(url)
#
#         # Wait for a short period to avoid overwhelming the website
#         time.sleep(0.5)
#
#

# METHOD 3
