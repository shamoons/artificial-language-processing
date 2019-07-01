import os
import re
import tokenize
import io
import numpy as np
import re
import pygments
from pygments.lexers import JavascriptLexer, PythonLexer, JavaLexer


class CodeModel:
    def __init__(self, corpus, language):
        self.corpus_file = corpus
        self.tokens = []
        if language == 'javascript':
            self.lexer = JavascriptLexer()
        elif language == 'python':
            self.lexer = PythonLexer()
        elif language == 'java':
            self.lexer = JavaLexer()

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

    def tokenize(self, save_tokens=None, load_tokens=None):
        if load_tokens is not None:
            f = open(load_tokens, 'rb')
            self.tokens = np.load(f, allow_pickle=True)
            [print(token) for token in self.tokens]
            print(self.tokens)
            f.close()
            return self.tokens

        if save_tokens is not None:
            token_file = open(save_tokens, 'ab')

        tokens = np.array([], dtype='object')
        line_count = 0
        tokens_to_save = np.array([], dtype='object')
        with open(self.corpus_file) as infile:
            for line in infile:
                if line_count % 1000 == 0:
                    print("Line Count: ", line_count, '')
                    if save_tokens is not None:
                        np.save(token_file, tokens_to_save)
                        tokens_to_save = np.array([], dtype='object')
                line_count += 1
                line_tokens = pygments.lex(line + '\n', self.lexer)
                for line_token in line_tokens:
                    tokens = np.append(tokens, line_token[1])
                    tokens_to_save = np.append(tokens_to_save, line_token[1])
                if line_count % 10000 == 0:
                    print("\tToken Count: ", len(tokens))
        self.tokens = tokens

        if save_tokens is not None:
            np.save(token_file, tokens_to_save)
        return self.tokens

    def uniqueness_study(self, corpus_size=1000, runs=10):
        total_corpus_size = len(self.tokens)

        counter = []
        for i in range(runs):
            start_index = np.random.randint(0, total_corpus_size - corpus_size)
            end_index = start_index + corpus_size
            subcorpus = self.tokens[start_index: end_index]

            unique_tokens = np.unique(subcorpus)
            unique_count = len(unique_tokens)
            unique_percent = unique_count / len(subcorpus)
            counter.append(unique_percent)
        print("Corpus Size: ", corpus_size, ' / ',
              total_corpus_size, 'Runs: ', runs)
        print("\tAverage: ", np.average(counter))
        print("\tStd Dev: ", np.std(counter))
