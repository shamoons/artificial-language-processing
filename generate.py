import argparse
from CodeModel import CodeModel


parser = argparse.ArgumentParser(
    description='Generate text from a model on a corpus.')

parser.add_argument('--weights', dest='weights', default='models/python.hdf5',
                    help='Filename for the weights')

parser.add_argument('--corpus', dest='corpus', default='data/small.txt',
                    help='Filename for the corpus')

parser.add_argument('--seq_length', dest='seq_length', default=150,
                    help='Sequence length to look back on')

args = parser.parse_args()

codemodel = CodeModel(corpus=args.corpus,
                      seq_length=args.seq_length, weights=args.weights)
codemodel.generate()
