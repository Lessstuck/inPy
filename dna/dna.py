from cs50 import sys
import csv

if (len(sys.argv) <= 2) or (len(sys.argv) > 3):
    print("Usage: python dna.py data.csv sequence.txts")
    exit(1)
dbFileName = sys.argv[1]
dnaFileName = sys.argv[2]

# open csv file into dictionary
# from https://docs.python.org/3/library/csv.html
with open(dbFileName, newline='') as db:
    reader = csv.DictReader(db)
    # for row in reader:
        # print(row['name'], row['AGATC'])

# print(f"database: {dbFileName}")

# open DNA sequence file
with open(dnaFileName, "r") as seq:
    while True:
        name = seq.read()
        if not name:
            # End of File
            break
        # print(f"item: {name} length: {len(name)}")
    # parse sequence
    for i in range(0, (len(name) - 4)):
        nucleoByte = name[i:(i + 4)]
        print(f"nucleoByte: {nucleoByte}")

exit(0)