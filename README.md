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
After 12 epocks, gets stuck at `266s - loss: 9.8586 - acc: 0.3884 - val_loss: 9.7036 - val_acc: 0.3980`

### Experiment 3
* lr=0.05
* BATCH_SIZE=64
* SEQ_LENGTH=60
* No Dropout
* Switching from `categorical_cross_entropy` to `sparse_categorical_crossentropy` loss function