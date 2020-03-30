from cs50 import sys
import csv

# check number of arguments
if (len(sys.argv) <= 2) or (len(sys.argv) > 3):
    print("Usage: python dna.py data.csv sequence.txts")
    exit(1)
dbFileName = sys.argv[1]
dnaFileName = sys.argv[2]

# open csv file into dictionary
# from https://docs.python.org/3/library/csv.html
with open(dbFileName, newline='') as db:
    reader = csv.DictReader(db)
    # from Tyler at https://stackoverflow.com/questions/24962908/how-can-i-read-only-the-header-column-of-a-csv-file-using-python
    fieldNames = reader.fieldnames
    fieldNames.remove('name')
    print(fieldNames)

# open DNA sequence file
with open(dnaFileName, "r") as sequence:
    seq = sequence.read()

# parse sequence
repeatsMax = []
for i in range(0, (len(fieldNames))):
    repeatsMax.append(0)
    repeats = 0
    STR = fieldNames[i]
    lenSTR = len(STR)
    for j in range(0, (len(seq) - lenSTR)):  # counts repeats, not contiguous repeats
        if STR == seq[j:(j + lenSTR)]:
            repeats += 1
        repeatsMax[i] = max(repeatsMax[i], repeats)

print(repeatsMax)

# TODO compare repeatsMax with each person's STR pattern

exit(0)