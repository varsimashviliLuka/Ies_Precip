import pymysql
import csv

# Database connection
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="Ml@Root88",
    database="weather"
)

cursor = connection.cursor()

# SQL query
query = "SELECT * FROM weather_data WHERE precip_time > '2024-06-26' AND precip_time < '2024-06-28'"
cursor.execute(query)

# Fetch data
rows = cursor.fetchall()
# Write to CSV
output_file = '../weather_data_2024-06-26_2024-06-28.csv'

with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write headers
    writer.writerow([column[0] for column in cursor.description])  # Column names
    # Write data
    writer.writerows(rows)

cursor.close()
connection.close()

print(f"Data exported to {output_file}")
