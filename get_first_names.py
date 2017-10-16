# build a file named first_names.txt in the data directory from the female_first_names.dat
# and male_first_names.dat files.
# also build a last_names.txt file from the last_names.dat file.
import os
import sys

# make sure we kill the first_names.txt file so if this is run again, we don't end up
# with duplicates.
if os.path.isfile('data/first_names.txt'):
    try:
        os.remove('data/first_names.txt')
    except Exception as ex:
        print ex.message
        sys.exit(1)

# read the female_first_names.dat file into an array, then extend that array
# with the lines from mail_first_names.dat
with file('data/female_first_names.dat', 'r') as f:
    lines = f.readlines()
with file('data/male_first_names.dat', 'r') as f:
    lines.extend(f.readlines())

# strip out the names in the array elements and write that name, one per line, into first_names.txt
# all those function calls that build name are:
#   get the characters from 0-15
#   trim the string
#   lower case the string
#   capitalize the first letter
with file('data/first_names.txt', 'a') as f:
    for line in lines:
        name = line[0:15].strip().lower().capitalize()
        f.write(name + "\n")

# kill last_names.txt so if this is run again, we dont have duplicates
if os.path.isfile('data/last_names.txt'):
    try:
        os.remove('data/last_names.txt')
    except Exception as ex:
        print ex.message
        sys.exit(1)

# read in the name records
with file('data/last_names.dat') as f:
    lines = f.readlines()

# strip out the names in the array elements and write the names into last_names.txt
with file('data/last_names.txt', 'a') as f:
    for line in lines:
        name = line[0:15].strip().lower().capitalize()
        f.write(name + "\n")
