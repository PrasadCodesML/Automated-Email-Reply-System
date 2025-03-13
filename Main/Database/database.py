import mysql.connector
import pandas as pd

# MySQL connection details (update as needed)
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "12345678"  # Update with actual MySQL password
MAIN_DATABASE = "TE_Email_Custom_Database"

# Maximum value for BIGINT UNSIGNED in MySQL
MAX_BIGINT_UNSIGNED = 18446744073709551615

# Connect to MySQL server
conn = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD
)
cursor = conn.cursor()

# Delete the database if it exists, then create a new one
cursor.execute(f"DROP DATABASE IF EXISTS {MAIN_DATABASE}")
cursor.execute(f"CREATE DATABASE {MAIN_DATABASE}")
cursor.execute(f"USE {MAIN_DATABASE}")

# Load the Excel file
excel_file = "Cleaned_Email_dataset.xlsx"
xls = pd.ExcelFile(excel_file)
sheet_names = xls.sheet_names
print("Sheets found:", sheet_names)

# Function to map pandas dtypes to MySQL datatypes
def map_dtype(dtype, col_name):
    if col_name == "quote_id":
        return "BIGINT UNSIGNED"
    if pd.api.types.is_integer_dtype(dtype):
        return "INT"
    elif pd.api.types.is_float_dtype(dtype):
        return "FLOAT"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "DATETIME"
    else:
        return "VARCHAR(255)"

# Process each sheet in the Excel file
for sheet in sheet_names:
    print(f"\nProcessing sheet: {sheet}")
    df = pd.read_excel(excel_file, sheet_name=sheet)
    
    # Clean column names
    df.columns = (
        df.columns.str.strip()
                  .str.replace(" ", "_")
                  .str.replace("&", "and")
                  .str.lower()
    )
    
    # Process 'quote_id' column if it exists
    if 'quote_id' in df.columns:
        df['quote_id'] = pd.to_numeric(df['quote_id'], errors='coerce')
        df = df.dropna(subset=['quote_id'])
        df = df[df['quote_id'] >= 0]
        df = df[df['quote_id'] <= MAX_BIGINT_UNSIGNED]
        df['quote_id'] = df['quote_id'].astype('int64')
    
    # Generate table name
    table_name = sheet.strip().replace(" ", "_").lower()
    
    # Create table schema
    columns_def = [f"`{col}` {map_dtype(df[col].dtype, col)}" for col in df.columns]
    create_table_query = f"CREATE TABLE `{table_name}` ({', '.join(columns_def)})"
    cursor.execute(create_table_query)
    
    # Prepare data for insertion
    df = df.where(pd.notnull(df), None)
    placeholders = ", ".join(["%s"] * len(df.columns))
    columns_str = ", ".join([f"`{col}`" for col in df.columns])
    insert_query = f"INSERT INTO `{table_name}` ({columns_str}) VALUES ({placeholders})"
    data_tuples = [tuple(x) for x in df.to_numpy()]
    
    # Insert data with batch handling
    try:
        cursor.executemany(insert_query, data_tuples)
        conn.commit()
        print(f"Data inserted into '{table_name}' successfully.")
    except Exception as e:
        print(f"Error inserting into '{table_name}': {e}")
        for i, row in enumerate(data_tuples):
            try:
                cursor.execute(insert_query, row)
            except Exception as inner_e:
                print(f"Error inserting row {i}: {row} -> {inner_e}")
        conn.commit()

# Cleanup
cursor.close()
conn.close()
print("Data upload complete.")
