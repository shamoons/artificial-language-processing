# PyOctoscraper
A Python based scraper to download Python source code from Github and train an RNN to generate source code. I have no hopes that the code generated will be useful, or even valid, but it's a fun experiment nonetheless.

## Scraper

I could not find any dataset of source code, so I scraped it myself. The [scraper.py](scraper.py) does the magic. To keep things sane, we're only interested in `keras` code written in `python` that have more than 500 stars. The rationale being that well written code is more likely to be written correctly (not exactly proof, but a close enough approximation).

## Generation

A super big shoutout to [Max Woolf](http://minimaxir.com/) for creating the [textgenrnn](https://github.com/minimaxir/textgenrnn) package. It made my life considerably easier and I highly recommend it for quick and dirty projects.

## Experiment Log

### Experiment 1
* lr=0.1
* BATCH_SIZE=32
* SEQ_LENGTH=60
* No Dropout

#### Result
Seems to get stuck with `loss: 14.3951 - acc: 0.1069 - val_loss: 14.3999 - val_acc: 0.1066`

### Experiment 2
* lr=0.05
* BATCH_SIZE=16
* SEQ_LENGTH=60
* No Dropout

#### Result
After 12 epochs, gets stuck at `266s - loss: 9.8586 - acc: 0.3884 - val_loss: 9.7036 - val_acc: 0.3980`

### Experiment 3
* lr=0.05
* BATCH_SIZE=64
* SEQ_LENGTH=60
* No Dropout
* Switching from `categorical_cross_entropy` to `sparse_categorical_crossentropy` loss function
  
#### Result
After 14 epochs, `63s - loss: 15.9969 - acc: 0.0076 - val_loss: 15.9936 - val_acc: 0.0078`

### Experiment 4
* lr=0.075
* BATCH_SIZE=8
* SEQ_LENGTH=100
* No Dropout

#### Result
After 18 epochs, `719s - loss: 12.6027 - acc: 0.2182 - val_loss: 12.6131 - val_acc: 0.2176`

### Experiment 5
* lr=1
* BATCH_SIZE=8
* SEQ_LENGTH=100
* No Dropout
* Balancing Classes (https://stackoverflow.com/a/53397560/239879)

#### Result
After 40 epochs, `703s - loss: 11.1046 - sparse_categorical_accuracy: 0.3111 - val_loss: 11.0284 - val_sparse_categorical_accuracy: 0.3159`

### Experiment 6
* lr=2
* BATCH_SIZE=16
* SEQ_LENGTH=100
* No Dropout
* Added `clipnorm=1` to Adam
* Added `clipvalue=1` to Adam

### Result
After 28 epochs, `385s - loss: 15.9803 - sparse_categorical_accuracy: 0.0086 - val_loss: 16.0032 - val_sparse_categorical_accuracy: 0.0072`

### Experiment 7
* lr=1
* BATCH_SIZE=32
* SEQ_LENGTH=150
* No Dropout
* Changed `clipvalue=0.5` to Adam

### Result
After 38 epochs, `474s - loss: 14.0049 - sparse_categorical_accuracy: 0.1312 - val_loss: 13.8736 - val_sparse_categorical_accuracy: 0.1393`

### Experiment 8
* lr=0.001
* BATCH_SIZE=8
* SEQ_LENGTH=100
* No Dropout
* Changed `clipvalue=1` to Adam
* Cleaned up scraper.

### Result
After 23 epochs, `978s - loss: 2.5998 - sparse_categorical_accuracy: 0.4812 - val_loss: 4.0491 - val_sparse_categorical_accuracy: 0.4016`.
Accuracy went down from a peak of 8 epochs, `972s - loss: 0.5992 - sparse_categorical_accuracy: 0.8476 - val_loss: 2.5992 - val_sparse_categorical_accuracy: 0.6423`

### Experiment 9
* lr=0.001, decay=0.995
* BATCH_SIZE=64
* SEQ_LENGTH=150

### Result
After epoch 20, `1078s - loss: 3.4757 - sparse_categorical_accuracy: 0.5847 - val_loss: 3.4988 - val_sparse_categorical_accuracy: 0.5757`


### Experiment 10
* lr=0.001, decay=0.995
* BATCH_SIZE=128
* SEQ_LENGTH=150
* Added another `LSTM` block
* Added `save_best_only=True` to `ModelCheckpoint`

### Result
Running