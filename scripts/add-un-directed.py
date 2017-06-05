
from datetime import datetime
import sys
import csv

csv_row_delimiter = '\t'

inputPathFile   = ''
outputPathFile  = ''
graphType = '' #Directed Undirected 

def main():
    if(len(sys.argv) < 4):
        print(getTime() + 
        " Usage: python /path/to/file.py \
        /path/to/input.tsv \
        /path/to/output.tsv \
        [Undirected|Directed]")
        sys.exit()

    global inputPathFile, outputPathFile, graphType
    inputPathFile = sys.argv[1]
    outputPathFile = sys.argv[2]
    graphType = sys.argv[3]
    print(getTime() + "Start")
    writeOutFile()
    print(getTime() + "Stop")

def getTime():
    return "["+ str(datetime.now()) +"]"

def writeOutFile():
    with open(outputPathFile, 'w') as csvfile1:
        writer = csv.writer(csvfile1, delimiter=csv_row_delimiter)
        writer.writerow(['Source', 'Target', 'Type'])

        with open(inputPathFile, 'r') as csvfile2:
            reader = csv.reader(csvfile2, dialect='excel', delimiter=csv_row_delimiter)
            for row in reader:
                col1 = row[0].encode('utf-8')
                col2 = row[1].encode('utf-8')
                writer.writerow([col1, col2, graphType])


#EXECUTE
main()