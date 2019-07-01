import argparse
from CodeModel import CodeModel

parser = argparse.ArgumentParser()
parser.add_argument('--lang', required=True,
                    choices=['javascript', 'python', 'java'])

args = parser.parse_args()

language = args.lang

code_model = CodeModel(corpus=f"data/{language}.txt", language=language)
code_model.tokenize(load_tokens=f"data/{language}_tokens.npy")
code_model.uniqueness_study(corpus_size=1000, runs=100)
