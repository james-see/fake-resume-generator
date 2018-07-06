# fake-resume-generator
For FUN! Use at your own risk. No warranties, no exceptions. 

Licensed under the [WTFPL](http://www.wtfpl.net/). Have fun.

## example

Try this:

`python3 mark-cough.py -e 'waldensilverman@gmail.com' -n "Walden Silverman" -c 4 --font Times -p`

Current -h:

```
usage: mark-cough.py [-h] [-v] [-s] [-f FOLDER] [-c COUNTERMAX] [-n NAMER]
                     [-e EMAILER] [--font FONT] [-g GROUP] [-p]

Process documents to make them generative

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -s, --silent          silent running server mode, no output to screen
  -f FOLDER, --folder FOLDER
                        folder location
  -c COUNTERMAX, --countermax COUNTERMAX
                        max number of lines for markov to write
  -n NAMER, --namer NAMER
                        Full name to use for top of resume
  -e EMAILER, --emailer EMAILER
                        email to use for contact info for resume
  --font FONT           font-selector either Times, Georgia, or Courier
  -g GROUP, --group GROUP
                        add custom Group affiliation section
  -p, --pdf             Generate a PDF in addition to the html
  ```
  
