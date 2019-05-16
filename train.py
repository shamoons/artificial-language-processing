from tensorflow.python.client import device_lib
from textgenrnn import textgenrnn
print(device_lib.list_local_devices())

textgen = textgenrnn()
textgen.train_from_file('data/python.txt', num_epochs=1,
                        new_model=True, header=False)
textgen.generate(interactive=True, top_n=5)
