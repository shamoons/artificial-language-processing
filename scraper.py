import argparse
from Scraper import JSScraper
from Scraper import PythonScraper

parser = argparse.ArgumentParser()
parser.add_argument('--lang', required=True,
                    choices=['javascript', 'python'])

args = parser.parse_args()

if args.lang == 'python':
    scraper = PythonScraper(corpus_file='data/python.txt', page=0)
    extension = 'py'
elif args.lang == 'javascript':
    scraper = JSScraper(corpus_file='data/javascript.txt', page=0)
    extension = 'js'

repos = [0]
while len(repos) > 0:
    repos = scraper.search_repos(
        query='stars:>=500 fork:true language:' + args.lang)
    print(repos)
    for repo in repos:
        scraper.get_contents(repo, file_extension=extension)
    scraper.next_page()
    print("Next page: ", scraper.page)
print("Done at page: ", scraper.page)


# import base64
# import os
# from Scraper import octoscrape

# o = octoscrape.Octoscrape(page=0)

# repos = [0]
# while len(repos) > 0:
#     repos = o.search_repos()
#     for repo in repos:
#         o.get_contents(repo, file_extension='py')
#     o.next_page()
#     print("Next page: ", o.page)
# print("Done at page: ", o.page)
