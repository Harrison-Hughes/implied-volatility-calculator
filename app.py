import sys
inFile = sys.argv[1]
outFile = sys.argv[2]


def manipulateData(lines):
    return lines


with open(inFile, 'r') as i:
    lines = i.readlines()

processedLines = manipulateData(lines)

with open(outFile, 'w') as o:
    for line in processedLines:
        o.write(line)
