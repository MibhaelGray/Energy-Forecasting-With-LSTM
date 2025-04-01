import pandas as pd
import os
import glob

# Directory containing the Excel files
data_dir = r"C:\Users\mgray\OneDrive\Documents\Energy Forecasting\Data"

# Output file path
output_file = os.path.join(data_dir, "All_ERCOT_Data.csv")

# Create an empty list to store dataframes
dfs = []

# Find all Excel files in the directory
excel_files = glob.glob(os.path.join(data_dir, "rpt*.xlsx"))

print(f"Found {len(excel_files)} Excel files to process")

# Process each Excel file
for file_path in excel_files:
    print(f"Processing file: {os.path.basename(file_path)}")
    
    # Get all sheet names in the Excel file
    try:
        xls = pd.ExcelFile(file_path)
        sheet_names = xls.sheet_names
        
        # Process each sheet (month) in the file
        for sheet_name in sheet_names:
            print(f"  Reading sheet: {sheet_name}")
            
            # Read the data from the sheet
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Check if the DataFrame has the expected columns
            expected_columns = ['Delivery Date', 'Delivery Hour', 'Delivery Interval', 
                               'Settlement Point Name', 'Settlement Point Type', 'Settlement Point Price']
            
            # Check column presence and handle variations in column names
            if not all(col in df.columns for col in expected_columns):
                print(f"  Warning: Sheet {sheet_name} doesn't have all expected columns. Attempting to normalize.")
                # Try to normalize column names by removing whitespace and case
                df.columns = [col.strip() for col in df.columns]
            
            # Filter for HB_NORTH rows only if you want just North Hub data
            if 'Settlement Point Name' in df.columns:
                north_hub_df = df[df['Settlement Point Name'] == 'HB_NORTH']
                if len(north_hub_df) > 0:
                    dfs.append(north_hub_df)
                    print(f"  Found {len(north_hub_df)} rows for HB_NORTH")
                else:
                    print(f"  No HB_NORTH data found in this sheet")
            else:
                print(f"  Warning: Settlement Point Name column not found in sheet {sheet_name}")
    
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

# Combine all dataframes
if dfs:
    print("Combining all data...")
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Ensure datetime format is consistent
    if 'Delivery Date' in combined_df.columns:
        combined_df['Delivery Date'] = pd.to_datetime(combined_df['Delivery Date'])
    
    # Sort by date and hour
    sort_columns = [col for col in ['Delivery Date', 'Delivery Hour', 'Delivery Interval'] 
                   if col in combined_df.columns]
    if sort_columns:
        combined_df = combined_df.sort_values(by=sort_columns)
    
    # Save to CSV
    print(f"Saving {len(combined_df)} rows to {output_file}")
    combined_df.to_csv(output_file, index=False)
    print("Done!")
else:
    print("No data found to combine.")