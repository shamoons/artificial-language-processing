from CodeModel import PyCode
from CodeModel import JSCode


py_codemodel = PyCode(corpus='data/python.txt', seq_length=10)
py_codemodel.tokenize()
# js_codemodel = JSCode(corpus='data/javascript.txt', seq_length=10)
# js_codemodel.tokenize()
