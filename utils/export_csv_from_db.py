import pymysql
import csv
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')

MYSQL_HOST = os.getenv('MYSQL_HOST', 'default_host')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'default_database')
MYSQL_USER = os.getenv('MYSQL_USER', 'default_user')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD_CSV', 'default_password')

start_date = '2024-06-26'
end_date = '2024-06-28'

# Database connection
connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)

cursor = connection.cursor()

# SQL query
query = f"SELECT * FROM weather_data WHERE precip_time > '{start_date}' AND precip_time < '{end_date}'"

cursor.execute(query)

# Fetch data
rows = cursor.fetchall()

# Write to CSV
output_file = f'../weather_data_{start_date}_{end_date}.csv'

with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write headers
    writer.writerow([column[0] for column in cursor.description])  # Column names
    # Write data
    writer.writerows(rows)

cursor.close()
connection.close()

print(f"Data exported to {output_file}")
