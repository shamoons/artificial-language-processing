from Trainer import trainer


t = trainer.Trainer('data/small.txt', weights='model/python.hdf5')
t.generate()

# print(t.filecontents[:200])
