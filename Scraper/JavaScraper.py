import re
import javalang
from .BaseScraper import BaseScraper


class JavaScraper(BaseScraper):

    def _clean_code(self, code):
        try:
            code = self._remove_comments(code)
            javalang.parse.parse(code)
            return code
        except Exception as e:
            print("ERROR", e)
            print(code)
            print("\n=======\n")
            return ''

    def _remove_comments(self, code):
        def replacer(match):
            s = match.group(0)
            if s.startswith('/'):
                return " "  # note: a space and not an empty string
            else:
                return s
        pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE
        )
        code = re.sub(pattern, replacer, code)
        return code
