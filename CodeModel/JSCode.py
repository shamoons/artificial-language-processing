import numpy as np
from pygments.lexers import JavascriptLexer
from .CodeModel import CodeModel


class JSCode(CodeModel):
    def tokenize(self, lexer=None, save_tokens=None):
        print("HERE I AM!", save_tokens)
        # lexer = JavascriptLexer()
        # super().tokenize(lexer=lexer, save_tokens=save_tokens)
