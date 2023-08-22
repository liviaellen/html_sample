import streamlit as st
import pandas as pd
import os
import plotly.express as px
from app import process_html_files
from datetime import datetime

def get_files_in_folder(folder):
    files = [file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]
    return sorted(files)

def main():
    st.title("HTML Table Extractor and Visualizer")

    input_folder = "data"  # Default input folder
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    folders = sorted(os.listdir(output_folder), reverse=True)
    default_output_folder = os.path.join(output_folder, folders[0]) if folders else output_folder

    st.text_input("Enter output folder where CSVs are saved:", default_output_folder)

    # Start the extraction process
    if st.button("Start Extraction"):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        new_output_folder = os.path.join(output_folder, f"output_{timestamp}")
        st.write("Extracting tables from HTML files...")
        logs = process_html_files(input_folder, new_output_folder)
        st.write("Extraction completed!")
        for log in logs:
            st.write(log)

    # Display the dataframes and log file
    if st.button("Visualize"):
        folders = sorted(os.listdir(output_folder), reverse=True)
        selected_document = st.selectbox("Select a document:", folders)
        st.write(f"Selected document: {selected_document}")

        selected_document_folder = os.path.join(output_folder, selected_document)
        csv_files = get_files_in_folder(selected_document_folder)
        selected_csv = st.selectbox("Select a CSV file:", csv_files)
        st.write(f"Selected CSV file: {selected_csv}")

        df = pd.read_csv(os.path.join(selected_document_folder, selected_csv))
        st.write(df)

        st.subheader("Log File:")
        log_files = [file for file in get_files_in_folder(output_folder) if file.endswith('_log.csv')]
        if log_files:
            log_file = log_files[0]
            log_df = pd.read_csv(os.path.join(output_folder, log_file))
            st.write(log_df)

        # Visualize dataframe
        if st.checkbox("Show visualization"):
            columns = df.columns
            x_axis = st.selectbox("Select X-axis:", columns)
            y_axis = st.selectbox("Select Y-axis:", columns)
            fig = px.line(df, x=x_axis, y=y_axis)
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
