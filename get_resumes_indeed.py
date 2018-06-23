#!/usr/local/bin/python3
'''
Gather resumes for fun and profit.
'''

# imports

import requests
from bs4 import BeautifulSoup
import argparse
from os.path import expanduser
import random
import uuid
from time import sleep
import os

# globals

URL = 'https://indeed.com'
homepath = expanduser("~")
pathsnippet = '/resumes?q={}'

# arguments handler
parser = argparse.ArgumentParser(description="Ways to interact with resume data from indeed.com")
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-s", "--silent", help="silent running server mode, no output to screen",
                    action="store_true")
parser.add_argument("-t", "--topic", help="resume topic", default="python")
args = parser.parse_args()
if args.verbose and not args.silent:
    print("verbosity turned on")


# functions

def get_links():
    '''
    Get links of resume pages from indeed.
    '''
    listoflinks = []
    r = requests.get(URL+pathsnippet.format(args.topic))
    if args.verbose:
        print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    if args.verbose:
        print(soup.find_all('a'))
    for a in soup.find_all('a'):
        if a.get('href').endswith('0') and a.get('href').startswith('/'):
            listoflinks.append(a.get('href'))
            if args.verbose:
                print(a.get('href'))
    return listoflinks
        

def main():
    resume_links = get_links()
    # exit('works so far')
    for link in resume_links:
        sleep(random.randint(1, 3))
        r = requests.get(URL+link)
        soup = BeautifulSoup(r.text)
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        justtext = '\n'.join(chunk for chunk in chunks if chunk)
        if not os.path.exists("{}/{}".format(homepath, "resumes")):
            os.makedirs("{}/{}".format(homepath, "resumes"))
        uniqq = uuid.uuid1()
        with open("{}/{}/{}.html".format(homepath, "resumes", uniqq), 'w') as f:
            f.write(r.text)
            if args.verbose:
                print('Saved {}.html successfully.'.format(uniqq))
        with open("{}/{}/{}.txt".format(homepath, "resumes", uniqq), 'w') as f:
            f.write(justtext)

# main

if __name__ == "__main__":
    main()