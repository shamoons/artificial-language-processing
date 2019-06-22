import numpy as np
from pygments.lexers import JavascriptLexer
from .CodeModel import CodeModel


class JSCode(CodeModel):
    def tokenize(self, **kwargs):
        lexer = JavascriptLexer()
        super().tokenize(lexer, **kwargs)
