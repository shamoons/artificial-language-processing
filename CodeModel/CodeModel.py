import os
import re
import tokenize
import io
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dropout, Dense, Activation


class CodeModel:
    def __init__(self, corpus, seq_length=100):
        self._corpus = corpus
        self.SEQ_LENGTH = seq_length
        self._load_corpus()
        self._build_model()

    def _build_model(self, weights=None):
        model = Sequential()
        model.add(Embedding(input_dim=len(self._tokens), output_dim=1024))

        model.add(LSTM(128))

        model.add(Dropout(rate=0.5))
        model.add(Dense(len(self._tokens)))
        model.add(Activation('softmax'))

        if weights != None:
            exists = os.path.isfile(weights)

            if exists:
                model.load_weights(weights, by_name=True)

        model.compile(loss='sparse_categorical_crossentropy',
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

    def train(self):
        self._model.fit(self.source_code, self.next_tokens, epochs=500,
                        verbose=2, batch_size=10, shuffle=True, validation_split=0.1)
