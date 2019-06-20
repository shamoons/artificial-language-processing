import argparse
from Scraper import JSScraper
from Scraper import PythonScraper
from Scraper import JavaScraper

parser = argparse.ArgumentParser()
parser.add_argument('--lang', required=True,
                    choices=['javascript', 'python', 'java'])

args = parser.parse_args()

if args.lang == 'python':
    scraper = PythonScraper(corpus_file='data/python.txt', page=0)
    extension = 'py'
elif args.lang == 'javascript':
    scraper = JSScraper(corpus_file='data/javascript.txt', page=0)
    extension = 'js'
elif args.lang == 'java':
    scraper = JavaScraper(corpus_file='data/java.txt', page=0)
    extension = 'java'


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
