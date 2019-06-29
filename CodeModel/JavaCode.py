import numpy as np
from pygments.lexers import JavaLexer
from .CodeModel import CodeModel


class JavaCode(CodeModel):
    def tokenize(self, save_tokens=None, load_tokens=None):
        lexer = JavaLexer()
        super().tokenize(lexer=lexer, load_tokens=load_tokens, save_tokens=save_tokens)
