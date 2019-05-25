import base64
import os
from Scraper import octoscrape

o = octoscrape.Octoscrape()

repos = [0]
page = 0
while len(repos) > 0:
    print("Page: ", page)
    repos = o.search_repos(page)
    for repo in repos:
        o.get_contents(repo, file_extension='.py')
    page += 1
