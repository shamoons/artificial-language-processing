import base64
import os
from Scraper import octoscrape

o = octoscrape.Octoscrape(page=0)

repos = [0]
while len(repos) > 0:
    repos = o.search_repos()
    print(repos)
    for repo in repos:
        o.get_contents(repo, file_extension='py')
    o.next_page()
    print("Next page: ", o.page)
print("Done at page: ", o.page)
