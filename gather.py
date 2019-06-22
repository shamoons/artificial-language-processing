from CodeModel import PyCode
from CodeModel import JSCode

print("Python")
py_codemodel = PyCode(corpus='data/python.1.txt', seq_length=10)
py_codemodel.uniqueness_study(corpus_size=100000, runs=100)
print("JavaScript")
js_codemodel = JSCode(corpus='data/javascript.1.txt', seq_length=10)
js_codemodel.uniqueness_study(corpus_size=100000, runs=100)
