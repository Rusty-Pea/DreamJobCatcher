import bs4 as bs
import requests
import urllib.parse
#
# # take companies and their urls from linkedin
#
#
#
# # navigate to 'about' site
# # go to website
#
#
# def company_url_retriever(links_linkedin_companies):
#     # Initialize the driver (e.g., for Chrome)
#     driver = webdriver.Chrome()
#
#     # Navigate to the webpage
#     driver.get(linkedin_search_url)
#
#     input("Opened web page. Log in if needed. Press enter when done.")
#
#     # get relevant elements from page
#     link_elements = driver.find_elements(By.CLASS_NAME, "app-aware-link")
#
#     # take the urls from these
#     link_elements_urls = [link_element.get_attribute('href') for link_element in link_elements]
#
#     # filter for only company urls
#     prefix = 'https://www.linkedin.com/company/'
#     links_linkedin_companies = list(set(list(filter(lambda x: x.startswith(prefix), link_elements_urls))))
#     print(str(len(links_linkedin_companies)) + ' companies found')
#     print(*links_linkedin_companies, sep='\n')
#
#
#
#
#
# primary_url = "https://www.linkedin.com/company/greentechco/"
# sess = requests.Session()
# sauce = sess.get(primary_url)
# soup = bs.BeautifulSoup(sauce.text, "html.parser")
#
# for form_list in soup.find_all('form'):
#
#     action_value = form_list.get('action')
#     action_url = urllib.parse.urljoin(primary_url, action_value)
#     method_value = form_list.get('method')
#
#     if (method_value == "post"):
#         payload = dict()
#
#         inputs1 = form_list.find_all('input',type ="email")
#         for i in inputs1:
#             input2 = i.get('name')
#             script_value = 'USER-EMAIL'
#             payload[input2] = script_value
#
#         inputs2 = form_list.find_all('input',type ="password")
#         for j in inputs2:
#             input3 = j.get('name')
#             script_value = 'PASSWORD-FOR-EMAIL'
#             payload[input3] = script_value
#
#         r = sess.post(action_url, data=payload)
#         with open("result_page.html", "w") as f:
#             f.write(str(r.content))
#
#
#

import requests
from lxml import html
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Log in to the website
login_url = "https://www.linkedin.com/in/aidan-goodall-a26929124/"
login_data = {
    "username": "aidangoodall7@gmail.com",
    "password": "jD8Kih5X"
}

with requests.Session() as session:
    # Send the login request and store the session cookies
    logging.info("Sending login request...")
    login_response = session.post(login_url, data=login_data)
    logging.info(f"Login response status code: {login_response.status_code}")

    # Check if the login was successful
    if login_response.status_code == 200:
        print("Login successful!")

        # Step 2: Open new links within the same domain
        while True:
            link = input("Enter a link within the same domain (or 'q' to quit): ")
            if link.lower() == 'q':
                break

            logging.info(f"Visiting link: {link}")
            # Send a request to the link using the authenticated session
            page_response = session.get(link)
            logging.info(f"Page response status code: {page_response.status_code}")


            # Parse the HTML content
            tree = html.fromstring(page_response.content)

            # Extract and print the page title
            title = tree.xpath('//title/text()')
            if title:
                title_text = title[0]
                logging.info(f"Title: {title_text}")
            else:
                logging.warning("Title not found in the HTML content.")

            # You can perform additional operations on the parsed HTML content here
            # ...

    else:
        print("Login failed.")
