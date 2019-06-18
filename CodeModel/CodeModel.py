import os
import re
import tokenize
import io
import numpy as np
import re
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
        # self.build_model()

    def _setup_callbacks(self):
        model_checkpoint = ModelCheckpoint(
            'models/python.hdf5', monitor='val_acc', save_best_only=True, save_weights_only=True)
        earlystopping_callback = EarlyStopping(
            monitor='val_acc', patience=10)
        return [model_checkpoint, earlystopping_callback]

    def build_model(self, weights=None):
        vocab_size = len(self._tokens) + 1
        model = Sequential()
        model.add(Embedding(input_dim=vocab_size,
                            output_dim=1024, input_length=self.SEQ_LENGTH))

        model.add(LSTM(128))

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

        self.filecontents = self._sanitize(filecontents)

        tokens = self._tokenize(filecontents)
        self.tokens_in_words = [token for token in tokens]

        self._tokens = set(self.tokens_in_words)

        self._word_indices = dict((c, i) for i, c in enumerate(self._tokens))
        self._indices_word = dict((i, c) for i, c in enumerate(self._tokens))

        self.source_code = []
        self.next_tokens = []

        sections = filecontents.split('<eos>')
        for section in sections:
            section_tokens = self._tokenize(section)
            section_text_in_words = [
                token for token in section_tokens if token != '']

            if len(section_text_in_words) < self.SEQ_LENGTH:
                continue

            i = 0
            next_token = ''

            while i < len(section_text_in_words) - self.SEQ_LENGTH:
                codeline = section_text_in_words[i: i + self.SEQ_LENGTH]
                next_token = section_text_in_words[i + self.SEQ_LENGTH]
                i += 1
                self.source_code.append(codeline)
                self.next_tokens.append(next_token)
            codeline = section_text_in_words[i: i + self.SEQ_LENGTH]
            next_token = '<eos>'
            self.source_code.append(codeline)
            self.next_tokens.append(next_token)

    def _sanitize(self, filecontents):
        filecontents = filecontents.replace("\n\n", "\n")
        filecontents = filecontents.replace('\n', ' \n ')
        filecontents = filecontents.replace('(', '( ')
        filecontents = filecontents.replace(')', ' ) ')
        filecontents = filecontents.replace('[', '[ ')
        filecontents = filecontents.replace(']', ' ]')
        filecontents = filecontents.replace(', ', ' , ')
        filecontents = re.sub(
            r'(?<![=!<>+-\/\*])(\=)(?![=!<>+-\/\*])', ' = ', filecontents)

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
        callbacks = self._setup_callbacks()
        source_code, next_tokens = self._encode(
            self.source_code, self.next_tokens)

        self._model.fit(source_code, next_tokens, epochs=500, callbacks=callbacks,
                        verbose=2, batch_size=self.BATCH_SIZE, shuffle=True, validation_split=0.1)

    def generate(self):
        next_word = "<s>"
        while next_word != "<eos>":
            x_pred = np.zeros((1, self.SEQ_LENGTH))
            preds = self._model.predict(x_pred, verbose=0)[0]
            next_index = np.argmax(preds)
            next_word = self._indices_word[next_index]
            print(next_index, next_word)
            print(preds, '===')
        # in_text, result = seed_text, seed_text
        # # generate a fixed number of words
        # for _ in range(n_words):
        #         # encode the text as integer
        #     encoded = tokenizer.texts_to_sequences([in_text])[0]
        #     encoded = array(encoded)
        #     # predict a word in the vocabulary
        #     yhat = model.predict_classes(encoded, verbose=0)
        #     # map predicted word index to word
        #     out_word = ''
        #     for word, index in tokenizer.word_index.items():
        #         if index == yhat:
        #             out_word = word
        #             break
        #     # append to input
        #     in_text, result = out_word, result + ' ' + out_word
        # return result

    def gather(self, corpus_size=1000, runs=200):
        total_corpus_size = len(self.tokens_in_words)

        counter = []
        for i in range(runs):
            start_index = np.random.randint(0, total_corpus_size - corpus_size)
            end_index = start_index + corpus_size
            corpus = self.tokens_in_words[start_index: end_index]

            unique_tokens = np.unique(corpus)
            unique_count = len(unique_tokens)
            unique_percent = unique_count / len(corpus)
            counter.append(unique_percent)
        print("Corpus Size: ", corpus_size, ' / ', total_corpus_size)
        print("\tAverage: ", np.average(counter))
        print("\tStd Dev: ", np.std(counter))
