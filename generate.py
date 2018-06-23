'''
Generate resume based on training set of sentences from resumes
'''
from os.path import expanduser
import os
import argparse

# globals

homepath = expanduser("~")

# arguments handler
parser = argparse.ArgumentParser(description="Process documents to make them generative")
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-s", "--silent", help="silent running server mode, no output to screen",
                    action="store_true")
parser.add_argument("-f", "--folder", help="folder location", default="resumes")
args = parser.parse_args()
if args.verbose and not args.silent:
    print("verbosity turned on")

# functions

def get_sentences(sample_folder):
    '''
    Get training data
    '''
    listofsentences = []
    for filename in os.listdir(sample_folder):
        if filename.endswith('txt'):
            with open("{}/{}".format(sample_folder, filename), 'r') as f:
                textfromdoc = f.read()
                listofsentences.extend(textfromdoc.split('.'))
                if args.verbose:
                    i = 1
                    while i < 10:
                        print(listofsentences[i])
                        i = i + 1
    return listofsentences


def main():
    '''
    Run the main program
    '''
    all_sentences = get_sentences("{}/{}".format(homepath,args.folder))
    if args.verbose:
        i = 1
        for sentence in all_sentences:
            print(sentence)
            i = i + 1
            if i > 100:
                break
    


# main

if __name__ == "__main__":
    main()