from googlesearch import search

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

careers_urls = [{"search term": "", "url": ""}]
        # 'https://www.zego.com/careers/',]

def google_search_from_linkedin_urls(urls):
    print('starting')
    # print(list(search('Google',num=2)))


    string_to_remove = "https://www.linkedin.com/company/"

    continue_search = True

    for url in urls:
        if not continue_search:
            break

        # TODO: add in extra words such as industry

        query_term = url.removeprefix(string_to_remove) + ' careers'
        print(f'searching for {query_term} ...')
        # TODO: work out why this is returning more than one result
        result = list(search(query_term, num=1))

        # include if needing to print all results
        # print(result)

        # return only first result
        print(result[0])
        careers_urls.append({"search term": query_term, "url": result[0]})

        while True:
            a = input("Press y to continue or q to quit: ")
            if a.lower() == 'y':
                break
            elif a.lower() == 'q':
                continue_search = False
                break
            else:
                print("Please press y or q:")

    return careers_urls
    print(careers_urls)


if __name__ == "__main__":
    # user_query = get_user_query()
    google_search_from_linkedin_urls(example_urls)

    print('Found the following urls:')
    for careers_url in careers_urls:
        print(careers_url['search term'] + ': ' + careers_url['url'] )



