from bs4 import BeautifulSoup
import pandas as pd
import os
import sys
import time
import datetime
import glob

def extract_tables_from_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    file_name = html_file.split('/')[-1].split('.')[0]
    tables = soup.find_all('table')
    return tables, file_name

def save_tables_to_csv(tables, file_name, output_folder):
    table_data = []
    for i, table in enumerate(tables):
        try:
            df = pd.read_html(str(table), header=0)[0]
        except ValueError as e:
            print(f'Error reading table {i} in {file_name}: {e}')
            continue
        table_data.append(df)

    merged_data = []
    current_table = table_data[0]
    for i in range(1, len(table_data)):
        if len(table_data[i].columns) == len(current_table.columns) and all(table_data[i].columns == current_table.columns):
            current_table = pd.concat([current_table, table_data[i]], ignore_index=True)
        else:
            merged_data.append(current_table)
            current_table = table_data[i]
    merged_data.append(current_table)

    for i, data in enumerate(merged_data):
        csv_file = os.path.join(output_folder, f'{file_name}_table_{i+1}.csv')
        data.to_csv(csv_file, index=False)
        print(f'Saved table {i+1} to {csv_file}')

def process_html_files(input_folder, output_folder):
    log_data = []
    log_messages = []

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    output_folder = os.path.join(output_folder, timestamp)
    os.makedirs(output_folder, exist_ok=True)

    html_files = glob.glob(os.path.join(input_folder, '*.html'))
    for i, html_file in enumerate(html_files):
        start_time = time.time()

        print(f'Processing {html_file}...')
        tables, file_name = extract_tables_from_html(html_file)
        if not tables:
            print(f'No tables found in {html_file}.')
            continue

        output_dir = os.path.join(output_folder, f'{str(i).zfill(4)}_{file_name}')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        save_tables_to_csv(tables, file_name, output_dir)

        elapsed_time = time.time() - start_time

        log_entry = {
            'datetime_execution': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'seconds_taken': elapsed_time,
            'number_of_tables_extracted': len(tables)
        }
        log_data.append(log_entry)

        log_messages.append(f"Processed {file_name}, extracted {len(tables)} tables, took {elapsed_time} seconds.")

    log_filename = os.path.join(output_folder, f"{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}_log.csv")
    log_df = pd.DataFrame(log_data)
    log_df.to_csv(log_filename, index=False)

    return log_messages


if __name__ == '__main__':
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    process_html_files(input_folder, output_folder)
