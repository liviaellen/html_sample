from bs4 import BeautifulSoup
import pandas as pd
import os
import glob
import re
import sys

def clean_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Find all elements that resemble table tags and rewrite them
    for tag in soup.find_all(True):
        if re.match(r'table|thead|tbody|tr|th|td', tag.name, re.IGNORECASE):
            tag.name = tag.name.lower()

    # Clean up any invalid attributes in the table tags
    for table in soup.find_all('table'):
        for attr in list(table.attrs.keys()):
            del table.attrs[attr]
        for tag in table.find_all(True):
            for attr in list(tag.attrs.keys()):
                del tag.attrs[attr]

    return soup


def extract_tables_from_html(html_file):
    soup = clean_html(html_file)
    tables = soup.find_all('table')
    return tables

def save_tables_to_csv(tables, output_folder):
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
        csv_file = os.path.join(output_folder, f'table_{i}.csv')
        data.to_csv(csv_file, index=False)
        print(f'Saved table {i} to {csv_file}')

def process_html_files(input_folder, output_folder):
    html_files = glob.glob(os.path.join(input_folder, '*.html'))
    for i, html_file in enumerate(html_files):
        print(f'Processing {html_file}...')
        html_name = os.path.basename(html_file).split('.')[0]
        folder_name = f'{str(i).zfill(4)}_{html_name}'
        output_dir = os.path.join(output_folder, folder_name)
        tables = extract_tables_from_html(html_file)
        save_tables_to_csv(tables, output_dir)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python app.py input_folder output_folder")
        sys.exit(1)
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    process_html_files(input_folder, output_folder)
