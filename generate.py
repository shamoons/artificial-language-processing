from CodeModel import CodeModel


codemodel = CodeModel(corpus='data/small.txt', seq_length=10)
codemodel.generate()
