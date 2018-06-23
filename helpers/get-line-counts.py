import os
from os.path import expanduser
import numpy as np

homepath = expanduser("~")

lines_list = []

# get line length  of each file in directory
for filename in os.listdir("{}/{}".format(homepath, 'resumes')):
    if filename.endswith('txt'):
        lines_list.append(sum(1 for line in open("{}/{}/{}".format(homepath, 'resumes', filename))))

# get average from list
print(np.mean(lines_list))