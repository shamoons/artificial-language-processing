import base64
import os
from Scraper import JSScraper

scraper = JSScraper.JSScraper(corpus_file='data/javascript.txt', page=0)


repos = [0]
while len(repos) > 0:
    repos = scraper.search_repos(
        query='stars:>=500 fork:true language:javascript')
    print(repos)
    for repo in repos:
        scraper.get_contents(repo, file_extension='js')
    scraper.next_page()
#     print("Next page: ", scraper.page)
# print("Done at page: ", scraper.page)
