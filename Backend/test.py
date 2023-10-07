import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password="Minha@99",
    database="openSourceData"
)

cursor = connection.cursor()

cursor.execute("SELECT version();")

# Fetch the result
result = cursor.fetchone()

print(f"Connected to PostgreSQL. Version: {result}")