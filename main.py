from bs4 import BeautifulSoup
import pandas as pd
import os

import sys
def extract_tables_from_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    file_name=html_file.split('/')[-1].split('.')[0]
    tables = soup.find_all('table')
    return tables,file_name

def save_tables_to_csv(tables, file_name, output_folder):
    table_data = []
    for i, table in enumerate(tables):
        df = pd.read_html(str(table), header=0)[0]
        table_data.append(df)

    # Check for tables that span multiple pages
    merged_data = []
    current_table = table_data[0]
    for i in range(1, len(table_data)):
        if len(table_data[i].columns) == len(current_table.columns) and all(table_data[i].columns == current_table.columns):
            current_table = pd.concat([current_table, table_data[i]], ignore_index=True)
        else:
            merged_data.append(current_table)
            current_table = table_data[i]
    merged_data.append(current_table)

    # Save the merged tables to CSV files
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for i, data in enumerate(merged_data):
        csv_file = os.path.join(output_folder, f'{file_name}_table_{i}.csv')
        data.to_csv(csv_file, index=False)
        print(f'Saved table {i} to {csv_file}')



if __name__ == '__main__':
    html_file = sys.argv[1]
    output_folder = 'output_folder'
    tables,file_name = extract_tables_from_html(html_file)
    save_tables_to_csv(tables,file_name, output_folder)
