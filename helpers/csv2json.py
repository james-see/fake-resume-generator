'''
Parse the stupid names.csv to names.json
'''

import csv  
import json    

with open( '../data/first_names.csv', 'r' )  as f:
    reader = csv.DictReader( f, fieldnames = ( "firstname" ))  
    out = json.dump( reader )  
    # print "JSON parsed!"  
with open( '../data/first_names.json', 'w') as f:
    f.write(out)

