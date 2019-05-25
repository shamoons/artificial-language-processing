import re
import base64
import os
import autopep8
import time
from dotenv import load_dotenv
from github import Github

load_dotenv()


class Octoscrape:
    def __init__(self, page=0):
        self.g = Github(os.environ['GITHUB_TOKEN'], retry=5)

    def search_repos(self, page=0):
        return self.g.search_repositories(
            query='keras stars:>=500 fork:true language:python', sort='stars', order='asc').get_page(page)

    def get_contents(self, repo, file_extension):
        try:
            contents = repo.get_contents("")
            print("Doing repo: ", repo.full_name, '\n')

            f = open("data/python.txt", "a")
            while len(contents) > 1:
                file_content = contents.pop(0)
                x_ratelimit_remaining = int(
                    file_content.raw_headers['x-ratelimit-remaining'])
                sleep_time = 0
                if x_ratelimit_remaining < 1000:
                    sleep_time = 1000 / x_ratelimit_remaining
                    print("Invoking sleep", sleep_time)
                    time.sleep(sleep_time)

                print('go')
                if file_content.type == "dir":
                    print("dir")
                    contents.extend(repo.get_contents(file_content.path))
                else:
                    print("file", file_content.path)
                    if file_content.path.endswith(file_extension):
                        written_file_content = '<s>\n'
                        written_file_content += "# " + repo.full_name + '\n'
                        written_file_content += "# " + file_content.path + '\n'
                        decoded_content = base64.b64decode(
                            file_content.content).decode('utf-8')
                        decoded_content = self._clean_code(decoded_content)
                        print(repo.full_name + "/" +
                              file_content.path,
                              "Rate: " + str(x_ratelimit_remaining),
                              "Code size: " + str(len(decoded_content)),
                              )
                        written_file_content += decoded_content
                        written_file_content += "<eos>\n"
                        if len(written_file_content) > 500:
                            f.write(written_file_content)
            f.close()
        except Exception as e:
            print(e)
            print(repo.full_name + "/" +
                  file_content.path, x_ratelimit_remaining)
            time.sleep(1)
            pass

    def _clean_code(self, code):
        code = re.sub(r'(?m)^ *#.*\n?', '', code)
        return autopep8.fix_code(code, options={'ignore': ['E501'], 'aggressive': 2})
