import re
import base64
import os
import autopep8
import time
import github
from dotenv import load_dotenv
from github import Github
from github import enable_console_debug_logging

# enable_console_debug_logging()

load_dotenv()


class Octoscrape:
    def __init__(self, page=0, min_code_size=300):
        self.g = Github(login_or_token=os.environ['GITHUB_TOKEN'], retry=5)
        self.page = page
        self.MIN_CODE_SIZE = min_code_size

    def _delay(self):
        if self.g.rate_limiting[0] < 15:
            delay = 15 / self.g.rate_limiting[0]
            print("Invoking Sleep: ", delay)
            time.sleep(delay)
        return

    def search_repos(self):
        return self.g.search_repositories(
            query='torch stars:>=1000 fork:true language:python').get_page(self.page)

    def get_contents(self, repo, file_extension):
        try:
            query = "size:>" + str(self.MIN_CODE_SIZE)
            f = open("data/python.txt", "a")
            code_files = self.g.search_code(
                query=query, extension="py", repo=repo.full_name)
            for code_file in code_files:
                print(repo.full_name + "/" + code_file.path)
                self._delay()
                decoded_content = base64.b64decode(
                    code_file.content).decode('utf-8')
                decoded_content = self._clean_code(decoded_content)
                if len(decoded_content) > self.MIN_CODE_SIZE:
                    print("\tCode size: ", len(decoded_content))
                    written_file_content = "# " + repo.full_name + "\n"
                    written_file_content += "# " + code_file.path + "\n"
                    written_file_content += decoded_content
                    written_file_content += "<eos>\n"
                    f.write(written_file_content)
            f.close()

        except Exception as e:
            print("Error: ", e)
        return
        try:
            contents = repo.get_contents("")
            written_file_content = '<s>\n'

            f = open("data/python.txt", "a")
            while len(contents) > 1:
                file_content = contents.pop(0)

                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))
                else:
                    if file_content.path.endswith(file_extension):
                        decoded_content = base64.b64decode(
                            file_content.content).decode('utf-8')
                        decoded_content = self._clean_code(decoded_content)
                        print("Code size: ", len(decoded_content))
                        written_file_content += decoded_content
                        written_file_content += "<eos>\n"
                        if len(written_file_content) > 300:
                            f.write(written_file_content)
            f.close()
        except:
            time.sleep(1)
            pass

    def _clean_code(self, code):
        code = re.sub(r'(?m)^ *#.*\n?', '', code)
        return autopep8.fix_code(code, options={'ignore': ['E501'], 'aggressive': 2})

    def next_page(self):
        self.page += 1
