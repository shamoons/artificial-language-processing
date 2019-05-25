import argparse
from tensorflow.python.client import device_lib
from CodeModel import CodeModel

print(device_lib.list_local_devices())

parser = argparse.ArgumentParser(description='Train a model on a corpus.')

parser.add_argument('--corpus', dest='corpus', default='data/small.txt',
                    help='Filename for the corpus')

parser.add_argument('--seq_length', dest='seq_length', default=100,
                    help='Start Index')


args = parser.parse_args()

codemodel = CodeModel(corpus=args.corpus, seq_length=args.seq_length)
codemodel.train()
