from cs50 import sys
import csv

# check number of arguments
if (len(sys.argv) < 2) or (len(sys.argv) > 2):
    print("Usage: python import.py data.csv")
    exit(1)
dbFileName = sys.argv[1]

# load database into dictionary
dbDictReader = csv.DictReader(open(dbFileName, newline=''))
STRlist = dbDictReader.fieldnames
name = STRlist[0]

for row in dbDictReader:
    # print(row.get('name'))
    fullName = row.get('name')
    names = fullName.split()

    if len(names) == 3:
        first = names[0]
        middle = names[1]
        last = names[2]
        print(first, middle, last)
    elif len(names) == 2:
        first = names[0]
        middle = '\\N'
        last = names[1]
        print(first, middle, last)
    else:
        print('names must be 2 or 3 words')