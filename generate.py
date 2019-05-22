from CodeModel import CodeModel


codemodel = CodeModel(corpus='data/python.txt', seq_length=10)
codemodel.generate()
