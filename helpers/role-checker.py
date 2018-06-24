'''
On keypress, keep generating new roles and see what Markov comes up with.
'''
# imports
import pickle
import markovgen
import argparse
import cv2

# globals

OKGREEN = '\033[92m'
ENDC = '\033[0m'

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

def generate_role(roles):
    '''
    Generate role on keypress.
    '''
    i = 'yes'
    mk = markovgen.Markov(roles)
    while i != 'q':
        newrole = mk.generate_markov_text()
        mk.feed(newrole)
        print('Mr Markov offers role: '+OKGREEN+'{}'.format(newrole)+ENDC)
        i = input('press any key to generate another role or "q" to exit...\n')
        print(mk.available_seeds())
    return


def main():
    with open('../data/ROLES.pickle', 'rb') as f:
        roles = pickle.load(f)
        if "Assault Vehicle Crew Member" in roles:
            print('yes')
            exit()
    generate_role(roles)


if __name__ == '__main__':
    main()