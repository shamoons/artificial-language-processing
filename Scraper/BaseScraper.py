import re
import base64
import os
import time
import github
import ast
import astunparse
from dotenv import load_dotenv
from github import Github
from github import enable_console_debug_logging

# enable_console_debug_logging()

load_dotenv()


class BaseScraper:
    def __init__(self, corpus_file, page=0, min_code_size=300):
        self.g = Github(login_or_token=os.environ['GITHUB_TOKEN'], retry=5)
        self.page = page
        self.MIN_CODE_SIZE = min_code_size
        self.CORPUS_FILE = corpus_file

    def _delay(self):
        if self.g.rate_limiting[0] < 15:
            delay = 15 / self.g.rate_limiting[0]
            print("Invoking Sleep: ", delay, self.g.rate_limiting[0])
            time.sleep(delay)
        return

    def search_repos(self, query):
        self._delay()
        return self.g.search_repositories(
            query=query, sort='stars', order='desc').get_page(self.page)

    def get_contents(self, repo, file_extension):
        try:
            query = "size:>" + str(self.MIN_CODE_SIZE)
            f = open(self.CORPUS_FILE, "a")
            code_files = self.g.search_code(
                query=query, extension=file_extension, repo=repo.full_name)
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
            time.sleep(1)
            pass

    def _clean_code(self, code):
        pass

    def next_page(self):
        self.page += 1
