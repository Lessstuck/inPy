from cs50 import sys
import csv

# check number of arguments
if (len(sys.argv) <= 2) or (len(sys.argv) > 3):
    print("Usage: python dna.py data.csv sequence.txts")
    exit(1)
dbFileName = sys.argv[1]
dnaFileName = sys.argv[2]

dbDictReader = csv.DictReader(open(dbFileName, newline=''))
STRlist = dbDictReader.fieldnames
# STRlist = fieldNames
STRlist.remove('name')
print(STRlist)

#  convert reader to dict
d = {}
for k in dbDictReader:
    # d[k] = v
    print(f"{k.get('AGATC')}")


# open DNA sequence file
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
print(f"repeatsMax: {repeatsMax}")
#  match STR lists

exit(0)