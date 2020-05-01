from cs50 import sys
import csv
from cs50 import SQL

# check number of arguments
if (len(sys.argv) < 2) or (len(sys.argv) > 2):
    print("Usage: python import.py data.csv")
    exit(1)
dbFileName = sys.argv[1]

db = SQL("sqlite:///students.db")

# load database into dictionary
dbDictReader = csv.DictReader(open(dbFileName, newline=''))

for row in dbDictReader:
    # print(row.get('name'))
    fullName = row.get('name')
    names = fullName.split()

    # convert 2 or 3 word names to 3 with/without None
    if len(names) == 3:
        first = names[0]
        middle = names[1]
        last = names[2]
    elif len(names) == 2:
        first = names[0]
        middle = None
        last = names[1]
    else:
        print('names must be 2 or 3 words')

    # copy house and birth
    house = row.get('house')
    birth = row.get('birth')

    # build database
    db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)", first, middle, last, house, birth)
exit()