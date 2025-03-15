import pandas as pd

def read_multiple_csv_files(file_paths):
    """Read multiple CSV files and return them as a list of DataFrames."""
    return [pd.read_csv(file_path) for file_path in file_paths]

def find_rows_by_product(dataframes, product_name):
    """Find rows containing a specific product across multiple DataFrames."""
    matching_rows = []
    
    for file_index, df in enumerate(dataframes):
        if 'product' not in df.columns.str.lower():
            continue
            
        # Get the actual column name with proper case
        product_col = df.columns[df.columns.str.lower() == 'product'][0]
        
        # Find matching rows
        matches = df[df[product_col].str.lower() == product_name.lower()]
        
        for idx, row in matches.iterrows():
            matching_rows.append({
                'file_index': file_index,
                'row_index': idx,
                'data': row.to_dict()
            })
    
    return matching_rows

def create_csv_with_selected_columns(matching_rows, output_file):
    """Create a new CSV file with only sales, date and region columns."""
    if not matching_rows:
        print("No matching rows found.")
        return
    
    # Extract the required data
    result_data = []
    for row in matching_rows:
        row_data = row['data']
        
        # Get column names with proper case
        price_col = next((col for col in row_data.keys() if col.lower() == 'price'), None)
        quantity_col = next((col for col in row_data.keys() if col.lower() == 'quantity'), None)
        date_col = next((col for col in row_data.keys() if col.lower() == 'date'), None)
        region_col = next((col for col in row_data.keys() if col.lower() == 'region'), None)
        
        if price_col and quantity_col and date_col and region_col:
            # Remove $ and convert to float
            price_value = row_data[price_col].replace('$', '') if isinstance(row_data[price_col], str) else row_data[price_col]
            sales = "${:.2f}".format(float(price_value) * float(row_data[quantity_col]))
            result_data.append({    
                'Sales': sales,
                'Date': row_data[date_col],
                'Region': row_data[region_col]
            })
    
    # Create a new DataFrame
    result_df = pd.DataFrame(result_data)
    
    # Save to CSV
    result_df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

# Example usage
file_paths = ['data/daily_sales_data_0.csv', 'data/daily_sales_data_1.csv', 'data/daily_sales_data_2.csv']
all_data = read_multiple_csv_files(file_paths)

# Find rows with product "pink morsel"
pink_morsel_rows = find_rows_by_product(all_data, "pink morsel")

# Display the found rows
for row_info in pink_morsel_rows:
    print(f"Found in file {file_paths[row_info['file_index']]}, row {row_info['row_index']}:")
    data = row_info['data']
    price_col = next((col for col in data.keys() if col.lower() == 'price'), None)
    quantity_col = next((col for col in data.keys() if col.lower() == 'quantity'), None)
    if price_col and quantity_col:
        # Remove $ and convert to float
        price_value = data[price_col].replace('$', '') if isinstance(data[price_col], str) else data[price_col]
        sales =  "${:.2f}".format(float(price_value) * float(data[quantity_col]))
        print(f"  Sales: {sales}")
        print(f"  Date: {data.get(next((col for col in data.keys() if col.lower() == 'date'), None))}")
        print(f"  Region: {data.get(next((col for col in data.keys() if col.lower() == 'region'), None))}")
    print()

# Create a new CSV file with the matching rows
create_csv_with_selected_columns(pink_morsel_rows, 'processeddata.csv')
