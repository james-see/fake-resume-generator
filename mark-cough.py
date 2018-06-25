'''
Generate markov chains resume
'''
import pickle
import markovgen
import argparse
from xhtml2pdf import pisa

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
  h2 { text-decoration: underline;}
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
    'Additional Information'
]

pickles = [
    'education',
    'skills',
    'other_info',
    'workexp'
]

resumeparts = dict()

# arguments handler
parser = argparse.ArgumentParser(description="Process documents to make them generative")
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-s", "--silent", help="silent running server mode, no output to screen",
                    action="store_true")
parser.add_argument("-f", "--folder", help="folder location", default="resumes")
parser.add_argument("-c", "--countermax", help="max number of lines for markov to write", default=3, type=int)
parser.add_argument("-n", "--namer", help="Full name to use for top of resume", default="Joe Smith")
parser.add_argument("-e", "--emailer", help="email to use for contact info for resume", default="joe.smith@blackhole.sun" )
parser.add_argument("--font", help="font-selector either Times, Georgia, or Courier", default='monospace')
parser.add_argument("-g", "--group", help="add custom Group affiliation section")
parser.add_argument("-p", "--pdf", help="Generate a PDF in addition to the html", action="store_true")
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
        with open('data/ROLES.pickle', 'rb') as f:
            roles = pickle.load(f)

        with open('data/{}.pickle'.format(item), 'rb') as f:
            readytext = pickle.load(f)
        #print(readytext[0])
        #exit()
        mk = markovgen.Markov(readytext)
        counter = 1
        while counter < counter_max:
            mkroles = markovgen.Markov(roles)
            newrole = mkroles.generate_markov_text()
            if item == 'Work Experience':
                roleline = '<h3 style="margin:5px 0 5px 0;">{}</h3>'.format(newrole)
            else:
                 roleline = ''
            line = mk.generate_markov_text() + '<br>'
            newtext.append(roleline+line)
            counter = counter + 1
        data[item] = ' '.join(newtext)
        if args.verbose:
            print(data[item])
    return data


def gen_text(data, name, email):

    with open('fresh_resume.html', 'w') as f:
        f.write('<!DOCTYPE html><head><style>h2 { text-decoration: underline; } body {font-family: '+args.font+'}'+cssdefault+'</style></head><body>')
        f.write('<div id="wrapper" style="text-align: center;"><div style="display:inline-block; margin-right:15px;"><h1>'+name+'</h1></div><div style="display:inline-block"><h2>'+email+'</h2></div></div>')
        for k, v in data.items():
            f.write('<h2 style="margin:0 0 10px 0;">{}</h2>'.format(k))
            # add markov new role from roles pickle above
            f.write('<span>{}</span>'.format(v))
        if args.group:
            f.write('<h2>Groups</h2>')
            f.write('<p>{}</p>'.format(args.group))
        f.write('</body></html>')
    return
def get_name():
    name = input('What name do you want to use? ')
    email = input('What email do you want to use? ')
    return name, email


def convertHtmlToPdf(sourceHtml, outputFilename):
    # open output file for writing (truncated binary)
    resultFile = open(outputFilename, "w+b")

    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(
            sourceHtml,                # the HTML to convert
            dest=resultFile)           # file handle to recieve result

    # close output file
    resultFile.close()                 # close output file

    # return True on success and False on errors
    return pisaStatus.err


def main():
    if args.namer == 'Joe Smith':
        name, email = get_name()
    else:
        name, email = args.namer, args.emailer
    resumedict = get_resume_parts() # load up the dict with the right keys
    alldata = pack_it_in(resumedict, args.countermax) # load up the keys with items
    gen_text(alldata, name, email)
    if args.pdf:
        with open('fresh_resume.html', 'r') as f:
            htmldata = f.read()
        convertHtmlToPdf(htmldata, 'fresh_resume.pdf')
# main

if __name__ == "__main__":
    main()