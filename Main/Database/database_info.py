import mysql.connector

# MySQL connection details (update as needed)
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "12345678"  # Update with actual MySQL password
MAIN_DATABASE = "TE_Email_Custom_Database"

# Connect to MySQL server and database
conn = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MAIN_DATABASE
)
cursor = conn.cursor()

# Retrieve all tables
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

print(f"Tables in database '{MAIN_DATABASE}':\n")

# Iterate through tables and print schema
for (table_name,) in tables:
    print(f"Table: {table_name}")
    cursor.execute(f"DESCRIBE {table_name}")
    columns = cursor.fetchall()
    print("Column Name | Data Type | Nullable | Key | Default | Extra")
    print("-" * 70)
    for col in columns:
        print(" | ".join(str(c) if c is not None else "NULL" for c in col))
    print("\n" + "=" * 70 + "\n")

# Cleanup
cursor.close()
conn.close()