from Trainer import trainer


t = trainer.Trainer('data/python.txt', weights='model/python.hdf5')
t.generate()

# print(t.filecontents[:200])
