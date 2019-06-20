import pygments
from pygments.lexers import JavascriptLexer
from .CodeModel import CodeModel


class JSCode(CodeModel):
    def tokenize(self):
        tokens = pygments.lex(self.filecontents, JavascriptLexer())

        simple_tokens = []
        for token in tokens:
            simple_tokens.append(token[1])

        self.all_tokens = simple_tokens

        return self.all_tokens
