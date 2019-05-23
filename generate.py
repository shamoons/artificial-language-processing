from CodeModel import CodeModel


codemodel = CodeModel(corpus='data/python.txt',
                      seq_length=60, weights='models/python.hdf5')
codemodel.generate()
