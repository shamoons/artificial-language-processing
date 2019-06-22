from CodeModel import PyCode
from CodeModel import JSCode
from CodeModel import JavaCode

# print("Python")
# py_codemodel = PyCode(corpus='data/python.1.txt', seq_length=10)
# py_codemodel.uniqueness_study(corpus_size=100000, runs=100)
# print("JavaScript")
# js_codemodel = JSCode(corpus='data/javascript.txt')
# js_codemodel.uniqueness_study(corpus_size=10, runs=100)

print("Java")
java_codemodel = JavaCode(corpus='data/java.txt')
java_codemodel.uniqueness_study(corpus_size=1000, runs=100, save_tokens='data/javatokens.npy')
