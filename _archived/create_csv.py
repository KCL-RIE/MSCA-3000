## RESOURCES ##
# https://stackoverflow.com/questions/41585078/how-do-i-read-and-write-csv-files

import csv

# Define data
# data_og_1 = [
#     ('2023-01-01','09:00','10:30'),
#     ('2023-01-01','13:00','14:30'),
#     ('2023-01-02','10:00','11:30'),
#     ('2023-01-03','15:00','16:30'),
#     ('2023-01-03','18:00','19:30'),
#     ('2023-01-03','20:00','21:30'),
# ]

# data_og_2 = [
#     ('2023-01-01','08:00','10:00'),
#     ('2023-01-02','13:00','14:30'),
#     ('2023-01-02','10:00','11:30'),
#     ('2023-01-03','19:30','20:30'),
# ]

# data_og_3 = [
#     ('2024-05-01','16:00','18:00'),
#     ('2023-04-15','11:00','14:30'),
#     ('2025-01-01','12:00','12:30'),
#     ('2022-11-30','11:30','13:30'),
# ]

data = [
    ('2022-11-30','15:00','17:37'),
    ('2023-01-01','13:25','14:32'),
    ('2023-01-01','16:00','16:45'),
    ('2023-01-01','18:00','18:30'),
]

# Write CSV file
with open("datetimes4.csv", "wt") as fp:
    writer = csv.writer(fp, delimiter=",")
    # writer.writerow(["your", "header", "foo"])  # write header
    writer.writerows(data)

# Read CSV file
with open("datetimes4.csv") as fp:
    reader = csv.reader(fp, delimiter=",", quotechar='"')
    # next(reader, None)  # skip the headers
    data_read = [row for row in reader]

print(data_read)
