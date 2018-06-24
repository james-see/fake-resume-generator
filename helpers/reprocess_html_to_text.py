from bs4 import BeautifulSoup, NavigableString
from os.path import expanduser
import os
import argparse
import re
import pickle

# globals
homepath = expanduser("~")
work_experience_p, education_p, skills_p, groups_p, other_information_p = [],[],[],[],[]

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

def reprocess(html):
    html = html.read()
    soup = BeautifulSoup(html, 'html.parser')
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    #text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    text = soup.get_text()
    return text

def html_to_text(html):
    "Creates a formatted text email message as a string from a rendered html template (page)"
    html = html.read()
    soup = BeautifulSoup(html, 'html.parser')
    # Ignore anything in head
    body, text = soup.body, []
    for element in body.descendants:
        # We use type and not isinstance since comments, cdata, etc are subclasses that we don't want
        if type(element) == NavigableString:
            # We use the assumption that other tags can't be inside a script or style
            if element.parent.name in ('script', 'style'):
                continue

            # remove any multiple and leading/trailing whitespace
            string = ' '.join(element.string.split())
            if string:
                if element.parent.name == 'a':
                    a_tag = element.parent
                    # replace link text with the link
                    string = a_tag['href']
                    # concatenate with any non-empty immediately previous string
                    if (    type(a_tag.previous_sibling) == NavigableString and
                            a_tag.previous_sibling.string.strip() ):
                        text[-1] = text[-1] + ' ' + string
                        continue
                elif element.previous_sibling and element.previous_sibling.name == 'a':
                    text[-1] = text[-1] + ' ' + string
                    continue
                elif element.parent.name == 'p':
                    # Add extra paragraph formatting newline
                    string = '\n' + string
                text += [string]
    doc = '\n'.join(text)
    # regex added after viewing data in verbose mode
    doc = re.sub(r'http\S+', '', doc)
    doc = re.sub(r'\/\S+', '', doc)
    doc = doc.replace('javascript:void0', '')
    doc = doc.replace('Find Resumes', '')
    doc = re.sub(r'Updated:\s.[a-z]+\s[0-9]+,\s[0-9]+', '', doc)
    if args.verbose:
        print(doc)
    return doc


def parse_by_id(html):
    '''
    Get text from fields
    '''
    html = html.read()
    soup = BeautifulSoup(html, 'html.parser')
    # get work experience
    try:
        workex = soup.find("div", {"id": "work-experience-items"}).text
        work_experience_p.append(workex)
    except:
        pass
    # get education
    try:
        education = soup.find("div", {"id": "education-items"}).text
        education_p.append(education)
    except:
        pass
    # get skills
    try:
        skills = soup.find("div", {"id": "skills-items"}).text
        skills_p.append(skills)
    except:
        pass
    # get groups
    try:
        groups = soup.find("div", {"id": "groups-items"}).text
        groups_p.append(groups)
    except:
        pass
    # get other information
    try:
        others = soup.find("div", {"id": "additionalinfo-items"}).text
        other_information_p.append(others)
    except:
        pass


def main():
    for filename in os.listdir("{}/{}".format(homepath,'resumes')):
        if filename.endswith('html'):
            with open("{}/{}/{}".format(homepath, "resumes", filename), 'r') as f:
                #textout = reprocess(f)
                #textout = html_to_text(f)
                parse_by_id(f)
    with open("../data/Work Experience.pickle", 'wb') as fb:
        pickle.dump(work_experience_p, fb)
    with open("../data/Skills.pickle", 'wb') as fb:
        pickle.dump(skills_p, fb)
    with open("../data/Education.pickle", 'wb') as fb:
        pickle.dump(education_p, fb)
    with open("../data/Groups.pickle", 'wb') as fb:
        pickle.dump(groups_p, fb)
    with open("../data/Additional Information.pickle", 'wb') as fb:
        pickle.dump(other_information_p, fb)       
            # with open("{}/{}/{}.txt".format(homepath, "resumes", filename.split('.')[0]), 'w') as f:
            #     f.write(textout)

# main

if __name__ == "__main__":
    main()