import csv

input_file = "rmp_data.csv"
output_file = "rmp1_data_without_empty_lines.csv"

with open(input_file, "r", newline="", encoding="utf-8") as file:
    csvreader = csv.reader(file)
    rows = [row for row in csvreader if any(cell for cell in row)]

with open(output_file, "w", newline="", encoding="utf-8") as file:
    csvwriter = csv.writer(file)
    csvwriter.writerows(rows)