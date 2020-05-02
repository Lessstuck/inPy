from cs50 import sys
from cs50 import SQL

# check number of arguments
if (len(sys.argv) < 2) or (len(sys.argv) > 3):
    print(f"{len(sys.argv)} arguments! Usage: python roster.py data.db")
    exit(1)
house = sys.argv[1]

# connect to database
db = SQL("sqlite:///students.db")

# create list of dicts of students in house
rows = db.execute("SELECT DISTINCT first, middle, last, house, birth FROM students WHERE house = ? ORDER BY last, first", house)

# copy values from each dict
for row in rows:
    birth = row.get('birth')
    first = row.get('first')
    middle = row.get('middle')
    last = row.get('last')

    # print middle name if it exists
    if middle == None:
        print(f"{first} {last}, born {birth}")
    else:
        print(f"{first} {middle} {last}, born {birth}")
exit()