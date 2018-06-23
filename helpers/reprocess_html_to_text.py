from bs4 import BeautifulSoup, NavigableString
from os.path import expanduser
import os
homepath = expanduser("~")

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
    return doc

def main():
    for filename in os.listdir("{}/{}".format(homepath,'resumes')):
        if filename.endswith('html'):
            with open("{}/{}/{}".format(homepath, "resumes", filename), 'r') as f:
                #textout = reprocess(f)
                textout = html_to_text(f)
            with open("{}/{}/{}.txt".format(homepath, "resumes", filename.split('.')[0]), 'w') as f:
                f.write(textout)

# main

if __name__ == "__main__":
    main()