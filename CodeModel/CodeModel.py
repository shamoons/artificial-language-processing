import os
import re
import tokenize
import io
import numpy as np
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dropout, Dense, Activation
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint, EarlyStopping


class CodeModel:
    def __init__(self, corpus, seq_length=100):
        self._corpus = corpus
        self.SEQ_LENGTH = seq_length
        self.BATCH_SIZE = 10
        self._load_corpus()
        self._build_model()

    def _setup_callbacks(self):
        model_checkpoint = ModelCheckpoint(
            'models/python.hdf5', monitor='val_acc', save_best_only=True, save_weights_only=True)
        earlystopping_callback = EarlyStopping(
            monitor='val_acc', patience=10)
        return [model_checkpoint, earlystopping_callback]

    def _build_model(self, weights=None):
        callbacks = self._setup_callbacks()
        vocab_size = len(self._tokens) + 1
        model = Sequential()
        model.add(Embedding(input_dim=vocab_size,
                            output_dim=1024, input_length=self.SEQ_LENGTH))

        model.add(LSTM(vocab_size))

        model.add(Dropout(rate=0.5))
        model.add(Dense(vocab_size - 1, activation='softmax'))
        print(model.summary())

        if weights != None:
            exists = os.path.isfile(weights)

            if exists:
                model.load_weights(weights, by_name=True)

        model.compile(loss='categorical_crossentropy',
                      optimizer="adam", metrics=['accuracy'])

        self._model = model

    def _load_corpus(self):
        file = open(self._corpus, 'r')
        filecontents = file.read()
        file.close()

        filecontents = self._sanitize(filecontents)

        tokens = self._tokenize(filecontents)
        text_in_words = [token for token in tokens if token != '']

        self._tokens = set(text_in_words)

        self._word_indices = dict((c, i) for i, c in enumerate(self._tokens))
        self._indices_word = dict((i, c) for i, c in enumerate(self._tokens))

        self.source_code = []
        self.next_tokens = []
        i = 0
        next_token = ''
        while next_token != '<eos>':
            codeline = text_in_words[i: i + self.SEQ_LENGTH]
            next_token = text_in_words[i + self.SEQ_LENGTH]
            i += 1
            self.source_code.append(codeline)
            self.next_tokens.append(next_token)

    def _sanitize(self, filecontents):
        filecontents = filecontents.replace("\n\n", "\n")
        filecontents = filecontents.replace('\n', ' \n ')

        return filecontents

    def _tokenize(self, filecontents):
        tokens = filecontents.split(' ')
        return tokens

    def _encode(self, x, y):
        sequences = np.array(x)
        next_tokens = np.array(y)

        encoded_sequences = []
        encoded_outputs = []
        for seq in sequences:
            encoded_sequence = []
            for token in seq:
                encoded_sequence.append(self._word_indices[token])
            categorial_sequence = to_categorical(
                encoded_sequence, num_classes=len(self._tokens))
            encoded_sequences.append(encoded_sequence)

        for next_token in next_tokens:
            encoded_outputs.append(self._word_indices[next_token])
        categorial_output = to_categorical(
            encoded_outputs, num_classes=len(self._tokens))

        return np.array(encoded_sequences), np.array(categorial_output)

    def train(self):
        source_code, next_tokens = self._encode(
            self.source_code, self.next_tokens)
        # print(source_code)
        print(source_code.shape)
        print(next_tokens.shape)
        # quit()

        self._model.fit(source_code, next_tokens, epochs=500,
                        verbose=2, batch_size=self.BATCH_SIZE, shuffle=True, validation_split=0.1)
