from duckduckgo_search import DDGS

def search_duckduckgo(query, max_results=10):
    links = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            if 'href' in r:
                links.append(r['href'])
            elif 'url' in r:
                links.append(r['url'])
    return links

# Example
results = search_duckduckgo("site:https://noid.dsn.dk", max_results=20)
for link in results:
    print(link)
