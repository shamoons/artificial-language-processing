import jsbeautifier
import re
from .BaseScraper import BaseScraper


class JSScraper(BaseScraper):
    def __init__(self, corpus_file, page=0):
        super().__init__(corpus_file=corpus_file, page=page)

    def _clean_code(self, code):
        def replacer(match):
            s = match.group(0)
            if s.startswith('/'):
                return " "  # note: a space and not an empty string
            else:
                return s
        code = jsbeautifier.beautify(code)

        pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE
        )
        code = re.sub(pattern, replacer, code)

        return code
