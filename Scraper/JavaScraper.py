import jsbeautifier
import re
import esprima
from .BaseScraper import BaseScraper


class JavaScraper(BaseScraper):

    def _clean_code(self, code):
        # code = self._remove_comments(code)
        return code
        try:
            esprima.parseScript(code)
            opts = jsbeautifier.default_options()
            opts.indent_size = 2
            opts.max_preserve_newlines = 1
            code = jsbeautifier.beautify(code, opts)
            code = self._remove_comments(code)

            return code
        except Exception as e:
            print("ERROR", e)
            print(code)
            print("\n=======\n")

        # return code

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
