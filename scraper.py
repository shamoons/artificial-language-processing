import base64
import os
from Scraper import octoscrape
# from dotenv import load_dotenv
# from github import Github

o = octoscrape.Octoscrape()

repos = [0]
while len(repos) > 0:
    repos = o.search_repos()
    for repo in repos:
        o.get_contents(repo, file_extension='.py')
    o.next_page()
# print(repos)

# load_dotenv()

# g = Github(os.environ['GITHUB_TOKEN'], retry=5)

# repositories = g.search_repositories(
#     query='stars:>=10 fork:true language:python').get_page(0)
# for repo in repositories:

#     contents = repo.get_contents("")
#     while len(contents) > 1:
#         file_content = contents.pop(0)

#         if file_content.type == "dir":
#             contents.extend(repo.get_contents(file_content.path))
#         else:
#             if file_content.path.endswith('.py'):
#                 decoded_content = base64.b64decode(
#                     file_content.content).decode('utf-8')
#                 print(decoded_content)

#     # print(repo)
