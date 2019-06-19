import pygments
from .CodeModel import CodeModel
from pygments.lexers import PythonLexer


class PyCode(CodeModel):
    def tokenize(self):
        tokens = pygments.lex(self.filecontents, PythonLexer())

        simple_tokens = []
        for token in tokens:
            simple_tokens.append(token[1])

        token_count = len(simple_tokens)
        unique_tokens = set(simple_tokens)

        print("Total Tokens: ", token_count)
        print("Unique Tokens: ", len(unique_tokens))

        return simple_tokens
