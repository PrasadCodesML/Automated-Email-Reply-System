import pandas as pd

# Path to your Excel file
excel_file = "Email_dataset.xlsx"

# Load the Excel file
xls = pd.ExcelFile(excel_file)

# Get the sheet names
sheet_names = xls.sheet_names

# Print the sheet names
print("Sheets found:", sheet_names)
