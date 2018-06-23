'''
Generate markov chains resume
'''

import markovgen
import argparse


# globals

cssdefault = """@media print {
  * { background: transparent !important; color: black !important; text-shadow: none !important; filter:none !important; -ms-filter: none !important; } /* Black prints faster: h5bp.com/s */
  a, a:visited { text-decoration: underline; }
  a[href]:after { content: " (" attr(href) ")"; }
  abbr[title]:after { content: " (" attr(title) ")"; }
  .ir a:after, a[href^="javascript:"]:after, a[href^="#"]:after { content: ""; }  /* Don't show links for images, or javascript/internal links */
  pre, blockquote { border: 1px solid #999; page-break-inside: avoid; }
  thead { display: table-header-group; } /* h5bp.com/t */
  tr, img { page-break-inside: avoid; }
  img { max-width: 100% !important; }
  @page { margin: 0.5cm; }
  p, h2, h3 { orphans: 3; widows: 3; }
  h2, h3 { page-break-after: avoid; }
}
"""
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

indeed_sections = [
    'Work Experience',
    'Education',
    'Skills',
    'Groups',
    'Additional Information'
]

resumeparts = dict()

# arguments handler
parser = argparse.ArgumentParser(description="Process documents to make them generative")
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-s", "--silent", help="silent running server mode, no output to screen",
                    action="store_true")
parser.add_argument("-f", "--folder", help="folder location", default="resumes")
parser.add_argument("-c", "--countermax", help="max number of lines for markov to write", default=3)
args = parser.parse_args()
if args.verbose and not args.silent:
    print("verbosity turned on")


# functions

def get_resume_parts():
    for item in indeed_sections:
        resumeparts[item] = ''
    if args.verbose:
        print(resumeparts)
    return resumeparts


def pack_it_in(data, counter_max):
    '''
    Generate new data based on old and put it into dict.
    '''
    for item in indeed_sections:
        newtext = []
        with open('data/{}.txt'.format(item), 'r') as f:
            readytext = f.read()
        mk = markovgen.Markov(readytext.split('.'))
        counter = 1
        while counter < counter_max:
            line = '\n' + mk.generate_markov_text()
            newtext.append(line)
            counter = counter + 1
        data[item] = ''.join(newtext)
        if args.verbose:
            print(data[item])
    return data


def gen_text(data, name, email):
    with open('fresh_resume.html', 'w') as f:
        f.write('<!DOCTYPE html><head><style>body {font-family: monospace;}'+cssdefault+'</style></head><body>')
        f.write('<div><h1>'+name+'</h1></div>')
        f.write('<h3>'+email+'</h3>')
        for k, v in data.items():
            f.write('<h2>{}</h2><br>'.format(k))
            f.write('<p>{}</p>'.format(v))
        f.write('</body></html>')

def get_name():
    name = input('What name do you want to use? ')
    email = input('What email do you want to use? ')
    return name, email

def main():
    name, email = get_name()
    resumedict = get_resume_parts() # load up the dict with the right keys
    alldata = pack_it_in(resumedict, args.countermax) # load up the keys with items
    gen_text(alldata, name, email)
# main

if __name__ == "__main__":
    main()