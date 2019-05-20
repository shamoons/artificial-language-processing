import argparse
from textgenrnn import textgenrnn

parser = argparse.ArgumentParser(description='Generate Text.')

parser.add_argument('--temperature', dest='temperature', default=0.5,
                    help='Temperature for generating text')

parser.add_argument('--weights', dest='weights',
                    help='Weights of the model')

parser.add_argument('--interactive', dest='interactive', default=False,
                    help='Interactive mode')

args = parser.parse_args()

textgen = textgenrnn(args.weights)
textgen.generate(interactive=args.interactive, temperature=args.temperature)
