from tensorflow.python.client import device_lib
from textgenrnn import textgenrnn
print(device_lib.list_local_devices())

textgen = textgenrnn()
textgen.train_from_file('data/small.txt', num_epochs=5, word_level=True, rnn_bidirectional=True,
                        rnn_layers=5, rnn_size=256,
                        new_model=True, header=False)
textgen.generate(interactive=True, top_n=5)
