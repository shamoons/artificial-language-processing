from textgenrnn import textgenrnn

textgen = textgenrnn()
textgen.train_from_file('data/python.txt', num_epochs=1)
textgen.generate(interactive=True, top_n=5)
