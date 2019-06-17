from CodeModel import CodeModel


codemodel = CodeModel(corpus='data/python.txt', seq_length=10)
codemodel.gather(corpus_size=1)
codemodel.gather(corpus_size=10)
codemodel.gather(corpus_size=100)
codemodel.gather(corpus_size=1000)
codemodel.gather(corpus_size=10000)
codemodel.gather(corpus_size=100000)
codemodel.gather(corpus_size=1000000)
