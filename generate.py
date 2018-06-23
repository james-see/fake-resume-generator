'''
Generate sample sentences data based on training set of sentences from resumes
'''
from os.path import expanduser
import os
import argparse
import re

# globals
pattern = re.compile(r'([A-Z].\w+\:)')
homepath = expanduser("~")
indeed_sections = [
    'Work Experience',
    'Education',
    'Skills',
    'Groups',
    'Additional Information'
]
standard_sections = [
    'system', 
    'server', 
    'tool', 
    'skill', 
    'project', 
    'responsibilities', 
    'objective',
    'location',
    'language',
    'framework',
    'description',
    'database',
    'service',
    'experience',
    'duties',
    'client',
    'framework',
    'fundamental',
    'interest',
    'package',
    'protocol',
    'role',
    'achievement',
    'cases',
    'coding',
    'libraries',
    'modules',
    'tech',
    'proficiency',
    'reference',
    'knowledge',
    'library',
    'design'
    ]

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

def parse_indeed_sections(resume_file):
    '''
    Use indeed's standards to split up sections.
    '''
    resumetext = resume_file.read()
    indeeddict = dict()
    for item in indeed_sections:
        neckdown = ''
        if item in resumetext:
            neckdown = resumetext.split(item)[1] # first step, remove crap from before heading
            if any(section in neckdown for section in indeed_sections):
                #if any(section in neckdown for section in indeed_sections):
                for section in indeed_sections:
                    try: neckdown.split(section)[0]
                    except:
                        continue
            if args.verbose:
                print(neckdown)
            indeeddict[item] = neckdown
            with open('data/{}.txt'.format(item),'a') as f:
                f.write("{}\n".format(indeeddict[item]))
    return indeeddict


def identify_sections(resume_file):
    '''
    Hopefully identify sections of a resume and chunk accordingly.
    For each section heading that conforms to standard_sections, create a text file.
    '''
    resumetext = resume_file.read()
    foundyou = re.findall(pattern, resumetext)
    if foundyou != None:
        if args.verbose:
            print("Found :! {}".format(foundyou))
        headingdict = dict()
        for heading in foundyou:
            if len(heading) < 4:
                continue
            headingdict[heading] = resumetext.split(heading)[1].split(':')[0] # lazy split next :
            if args.verbose:
                print(headingdict[heading]) # hopefully sections become apparant
            try:
                prepped_name = heading.split(' ')[1].lower()
            except:
                prepped_name = heading.split(':')[0].lower()
            if prepped_name.endswith(':'):
                prepped_name = prepped_name[:-1]
            while ' ' in prepped_name:
                prepped_name = prepped_name.split(' ')[1]
            prepped_name = ''.join(c for c in prepped_name if c.isalnum())
            # check for conforming to standards, otherwise move on
            if any(section in prepped_name for section in standard_sections):
                with open('data/{}.txt'.format(prepped_name),'a') as f:
                    f.write("{}\n".format(headingdict[heading]))
            # with open('data/{}.txt'.format(prepped_name),'a') as f:
            #     f.write("{}\n".format(headingdict[heading]))
    else:
        if args.verbose:
            print('No headings found.')
    return headingdict
    #sections = resumetext.split(':')



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
    # lets look for sections in the resumes
    for filename in os.listdir("{}/{}".format(homepath,args.folder)):
        if filename.endswith('txt'):
            with open("{}/{}".format("{}/{}".format(homepath,args.folder), filename), 'r') as f:
                #sections = identify_sections(f)
                indeedparse = parse_indeed_sections(f)
    exit('testing done')

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