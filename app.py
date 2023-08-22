from bs4 import BeautifulSoup
import pandas as pd
import os
import glob
import re
import sys
import datetime
import time

def clean_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Find all elements that resemble table tags and rewrite them
    for tag in soup.find_all(True):
        if re.match(r'table|thead|tbody|tr|th|td', tag.name, re.IGNORECASE):
            tag.name = tag.name.lower()

    # Clean up any invalid attributes in the table tags
    for table in soup.find_all('table'):
        table.attrs = {}
        for tag in table.find_all(True):
            tag.attrs = {}
    return soup

def extract_table_from_html(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table')
    if table is None:
        return None
    rows = table.find_all('tr')
    header = [th.text.strip() for th in rows[0].find_all('th')]
    data = []
    for row in rows[1:]:
        data.append([td.text.strip() for td in row.find_all('td')])
    df = pd.DataFrame(data, columns=header)
    return df

def extract_tables_from_html(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table')
    if table is None:
        return None

    rows = table.find_all('tr')
    header = [th.text.strip() for th in rows[0].find_all('th')]
    data = []

    # Skip the first row if there are headers, otherwise start from the first row
    start_index = 1 if header else 0

    for row in rows[start_index:]:
        data.append([td.text.strip() for td in row.find_all('td')])

    # If there are no headers, set header=None
    if not header:
        header = None

    df = pd.DataFrame(data, columns=header)
    return df


def save_tables_to_csv(tables, output_folder):
    # Filter out None values from the tables list
    tables = [table for table in tables if table is not None]
    for i, table in enumerate(tables):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        csv_file = os.path.join(output_folder, f'table_{i}.csv')
        table.to_csv(csv_file, index=False)
        print(f'Saved table {i} to {csv_file}')


def process_html_files(input_folder, output_folder):
    log_data = []

    html_files = glob.glob(os.path.join(input_folder, '*.html'))
    for i, html_file in enumerate(html_files):
        start_time = time.time()

        print(f'Processing {html_file}...')
        html_name = os.path.basename(html_file).split('.')[0]
        folder_name = f'{str(i).zfill(4)}_{html_name}'
        output_dir = os.path.join(output_folder, folder_name)
        tables = extract_tables_from_html(html_file)

        if tables is None:
            print(f'No tables found in {html_file}.')
            continue

        save_tables_to_csv(tables, output_dir)

        elapsed_time = time.time() - start_time

        log_data.append({
            'datetime_execution': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'seconds_taken': elapsed_time,
            'number_of_tables_extracted': len(tables)
        })

    # Save the log data to a CSV file with a name based on the current date and time
    log_filename = f"{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}_log.csv"
    log_df = pd.DataFrame(log_data)
    log_df.to_csv(log_filename, index=False)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python app.py input_folder output_folder")
        sys.exit(1)
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    process_html_files(input_folder, output_folder)
