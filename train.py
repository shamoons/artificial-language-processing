import argparse
import tensorflow
from tensorflow.python.client import device_lib
from textgenrnn import textgenrnn
print(device_lib.list_local_devices())

parser = argparse.ArgumentParser(description='Train on a datafile.')

parser.add_argument('--filename', dest='filename', default='data/small.txt',
                    help='Filename for the training file')

parser.add_argument('--name', dest='name', default='small_model',
                    help='Name of the trained model')


args = parser.parse_args()

textgen = textgenrnn()
textgen.train_from_file(args.filename, num_epochs=5, word_level=True, rnn_bidirectional=True,
                        rnn_layers=5, rnn_size=256, name=args.name,
                        new_model=True, header=False)
