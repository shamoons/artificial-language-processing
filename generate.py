from CodeModel import CodeModel


codemodel = CodeModel(corpus='data/python.txt', seq_length=25)
codemodel.generate()
