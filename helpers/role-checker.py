'''
On keypress, keep generating new roles and see what Markov comes up with.
'''
# imports
import pickle
import markovgen
import argparse
import cv2

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
    while True:
        input('press any key to generate another...\n')
        k = cv2.waitKey(1) & 0xFF
        # press 'q' to exit
        if k == ord('q'):
            break
        else:
            mk = markovgen.Markov(roles)
            newrole = mk.generate_markov_text()
            print('Mr Markov offers role: {}'.format(newrole))
            input('press any key to generate another...\n')
    return


def main():
    with open('../data/ROLES.pickle', 'rb') as f:
        roles = pickle.load(f)
    generate_role(roles)


if __name__ == '__main__':
    main()