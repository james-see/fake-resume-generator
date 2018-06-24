'''
Get list of roles and pickle it for mr markov later.
'''
from bs4 import BeautifulSoup
import requests
import argparse
import os
import pickle

# globals

# list of over 1000 roles
urltograb = 'https://www.careerplanner.com/ListOfJobs.cfm'

# arguments handler
parser = argparse.ArgumentParser(description="Process documents to make them generative")
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-s", "--silent", help="silent running server mode, no output to screen",
                    action="store_true")
args = parser.parse_args()
if args.verbose and not args.silent:
    print("verbosity turned on")

# functions

def get_it(urltograb):
    '''
    Get list of roles from website and pickle into data file.
    '''
    r = requests.get(urltograb).content
    soup = BeautifulSoup(r, 'html.parser')
    alla = soup.find_all('a')
    roles_list = []
    for item in alla:
        if 'Jobs' in item.text and 'OR' not in item.text and ' and ' not in item.text:
            if args.verbose:
                print(item.text.split(' Jobs')[0])
            # write to a list asshole
            roles_list.append(item.text.split(' Jobs')[0].strip())
        else:
            continue
    # pickle that shit
    with open("../data/ROLES.pickle", 'wb') as fb:
        pickle.dump(roles_list, fb)

def main():
    get_it(urltograb)


if __name__ == '__main__':
    main()