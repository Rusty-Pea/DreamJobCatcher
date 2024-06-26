from googlesearch import search

def google_search_from_linkedin_urls(urls):
    careers_urls = []

    string_to_remove = "https://www.linkedin.com/company/"

    continue_search = True

    for url in urls:
        if not continue_search:
            break

        # TODO: add in extra words such as industry

        query_term = url.removeprefix(string_to_remove).removesuffix('/') + ' careers'
        print(f'searching for {query_term} ...')
        # TODO: work out why this is returning more than one result
        result = list(search(query_term))
        # print(result[0])
        if len(result) == 0:
            continue
        elif len(result) >=1:

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
