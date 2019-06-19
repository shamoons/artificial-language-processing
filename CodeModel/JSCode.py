import pygments
from pygments.lexers import JavascriptLexer
from .CodeModel import CodeModel


class JSCode(CodeModel):
    def tokenize(self):
        tokens = pygments.lex(self.filecontents, JavascriptLexer())

        simple_tokens = []
        for token in tokens:
            simple_tokens.append(token[1])

        token_count = len(simple_tokens)
        unique_tokens = set(simple_tokens)

        print("Total Tokens: ", token_count)
        print("Unique Tokens: ", len(unique_tokens))

        return simple_tokens
