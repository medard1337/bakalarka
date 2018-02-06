import csv

with open('11373.dat', 'r') as input_file:
    lines = input_file.readlines()
    newLines = []
    for line in lines:
        newLine = line.strip('').split()
        newLines.append(newLine)

with open('file.csv', 'w') as output_file:
    file_writer = csv.writer(output_file)
    file_writer.writerows(newLines)