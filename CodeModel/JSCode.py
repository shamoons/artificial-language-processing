import jsbeautifier
import re
from .CodeModel import CodeModel
# from subword_nmt.learn_bpe import learn_bpe
import sentencepiece as spm


class JSCode(CodeModel):
    def tokenize(self):
        s = spm.SentencePieceProcessor()
        # s.Load('test.model')
        spm.SentencePieceTrainer.Train(
            "--input=" + self._corpus + " --model_prefix=m --vocab_size=1000 --model_type=bpe --max_sentence_length=100000 --character_coverage=1")
        s.load('m.model')
        pieces = s.EncodeAsPieces(self.filecontents)
        outfile = open('outfile.txt', 'w')
        outfile.write("\n".join(pieces))

        decoded = s.DecodePieces(pieces)
        print(decoded)

        # print(pieces)
        # infile = open(self._corpus, 'r')
        # outfile = open('data/jsvocab.txt', 'a')
        # words = learn_bpe(infile, outfile=outfile, num_symbols=100)
        # print(words)
