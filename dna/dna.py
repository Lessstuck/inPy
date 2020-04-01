from cs50 import sys
import csv

# check number of arguments
if (len(sys.argv) <= 2) or (len(sys.argv) > 3):
    print("Usage: python dna.py data.csv sequence.txts")
    exit(1)
dbFileName = sys.argv[1]
dnaFileName = sys.argv[2]

# load database into dictionary
dbDictReader = csv.DictReader(open(dbFileName, newline=''))
STRlist = dbDictReader.fieldnames

# load DNA sequence file
with open(dnaFileName, "r") as sequence:
    seq = sequence.read()
lenSEQ = len(seq)

# parse sequence
repeatsMax = []
for i in range(0, (len(STRlist))):
    repeatsMax.append(0)
    repeats = 0
    STR = STRlist[i]
    lenSTR = len(STR)
    j = 0
    while j + lenSTR < lenSEQ:
        while seq[j:(j + lenSTR)] == STR:
            repeats += 1
            j += lenSTR
        repeatsMax[i] = max(repeatsMax[i], repeats)
        j += 1
del repeatsMax[0]  # remove name element

#  match STR lists
for row in dbDictReader:
    dbRecords = []
    for k in range(1, (len(STRlist))):  # starts at 1 to skip name field
        dbRecords.append(int(row[STRlist[k]]))
    # print(f"{dbRecords} {repeatsMax}")
    if dbRecords == repeatsMax:
        print(f"{row[STRlist[0]]}")
        exit(0)
print("No match")
exit(0)