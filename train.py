from tensorflow.python.client import device_lib
from CodeModel import CodeModel

print(device_lib.list_local_devices())

codemodel = CodeModel(corpus='data/python.txt')
codemodel.train()
