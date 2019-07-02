import argparse
from CodeModel import CodeModel

parser = argparse.ArgumentParser()
parser.add_argument('--lang', required=True,
                    choices=['javascript', 'python', 'java'])
parser.add_argument('--save', required=False, default='False',
                    choices=['True', 'False'])
parser.add_argument('--load', required=False, default='False',
                    choices=['True', 'False'])


args = parser.parse_args()

language = args.lang

code_model = CodeModel(corpus=f"data/{language}.txt", language=language)
if args.save.lower() == 'true':
    code_model.tokenize(save_tokens=f"data/{language}_tokens.npy")
elif args.load.lower() == 'true':
    code_model.tokenize(load_tokens=f"data/{language}_tokens.npy")
code_model.uniqueness_study(corpus_size=1000, runs=100)
