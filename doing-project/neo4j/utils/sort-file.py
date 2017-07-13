import csv
import os

input_file_name = 'louvain.6'
output_file_name = 'louvain-sorted.6'

delimiter = ' '

inputPathFile = os.getcwd() + '/' + input_file_name
outputPathFile = os.getcwd() + '/' + output_file_name

rows_list = []

with open(inputPathFile, 'r') as csvfile2:
    reader = csv.reader(csvfile2, dialect='excel', delimiter=delimiter)
    for row in reader:
        rows_list.append(row)

rows_list_sorted = sorted(rows_list, key=len, reverse=True)

with open(outputPathFile, 'w') as csvfile1:
    writer = csv.writer(csvfile1, delimiter=delimiter)
    for id_list in rows_list_sorted:
        print(id_list)
        writer.writerow(id_list)

# END