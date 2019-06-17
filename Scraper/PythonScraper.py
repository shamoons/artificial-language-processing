import astunparse
import ast
from .BaseScraper import BaseScraper


class PythonScraper(BaseScraper):

    def _clean_code(self, code):
        try:
            parsed_code = ast.parse(code)
        except:
            return ''

        lines = astunparse.unparse(parsed_code).split('\n')
        new_code = ''
        for line in lines:
            if line.lstrip()[:1] not in ("'", '"'):
                new_code += line + '\n'

        return new_code
