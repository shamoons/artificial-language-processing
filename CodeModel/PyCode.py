import pygments
from .CodeModel import CodeModel
from pygments.lexers import PythonLexer


class PyCode(CodeModel):
    def tokenize(self):
        tokens = pygments.lex(self.filecontents, PythonLexer())

        simple_tokens = []
        for token in tokens:
            simple_tokens.append(token[1])

        self.all_tokens = simple_tokens

        return self.all_tokens
