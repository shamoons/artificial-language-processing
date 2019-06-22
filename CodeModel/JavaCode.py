import numpy as np
from pygments.lexers import JavaLexer
from .CodeModel import CodeModel


class JavaCode(CodeModel):
    def tokenize(self, *args):
        lexer = JavaLexer()
        super().tokenize(lexer)
