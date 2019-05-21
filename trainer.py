import tensorflow
from tensorflow.python.client import device_lib

from Trainer import trainer

print(device_lib.list_local_devices())


t = trainer.Trainer('data/python.txt')
t.train()
