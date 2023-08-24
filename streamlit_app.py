import streamlit as st
import os
import pandas as pd
import subprocess
import glob
import plotly.express as px

def show_dataframe(file_path):
    if file_path is None:
        st.warning("Please select a valid CSV file.")
        return None
    try:
        df = pd.read_csv(file_path)
        st.write(df)
        return df
    except Exception as e:
        st.error(f"Failed to load the DataFrame. Error: {e}")
        return None

def plot_dataframe(df):
    if df is None:
        st.warning("No DataFrame to visualize.")
        return

    columns = df.columns.tolist()
    x_axis = st.selectbox("Select the X-axis:", columns)
    y_axis = st.selectbox("Select the Y-axis:", columns)
    plot_type = st.selectbox("Select the plot type:", ["Line Plot", "Bar Chart", "Scatter Plot"])

    if plot_type == "Line Plot":
        fig = px.line(df, x=x_axis, y=y_axis)
    elif plot_type == "Bar Chart":
        fig = px.bar(df, x=x_axis, y=y_axis)
    else:
        fig = px.scatter(df, x=x_axis, y=y_axis)

    st.plotly_chart(fig)

def main():
    st.title("HTML Table Extraction Tool")

    # Step 1: Select Input Folder and Run HTML Extraction
    st.header("Step 1: Select Input Folder and Run HTML Extraction")
    input_folder = st.text_input("Enter the path to the input folder:", "data")
    if st.button("Run HTML Extraction"):
        st.write(f"Processing HTML files in '{input_folder}'...")
        process = subprocess.Popen(["make", "run", f"INPUT={input_folder}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            st.success(f"HTML files in '{input_folder}' have been processed.")
            st.write(f"Log output:\n{stdout.decode()}")
        else:
            st.error(f"Failed to process HTML files. Error:\n{stderr.decode()}")

    # Step 2: Select and Display CSV Files
    st.header("Step 2: Select and Display CSV Files")
    output_folder = st.text_input("Enter the path to the output folder:", "output")
    output_folders = glob.glob(os.path.join(output_folder, "*"))
    if not output_folders:
        st.warning("No output folders found.")
        return
    selected_output_folder = st.selectbox("Select the timestamped output folder:", output_folders)

    csv_files = glob.glob(os.path.join(selected_output_folder, "*/*.csv"))
    if not csv_files:
        st.warning("No CSV files found in the selected output folder.")
        return
    selected_csv = st.selectbox("Select a CSV file to visualize:", csv_files, index=0)
    df = show_dataframe(selected_csv)

    # Data Visualization
    st.header("Data Visualization")
    plot_dataframe(df)

    # Display Log File
    st.header("View Log File")
    log_files = glob.glob(os.path.join(selected_output_folder, "*_log.csv"))
    if log_files:
        log_file = log_files[0]
        if st.button("View Log"):
            show_dataframe(log_file)
    else:
        st.warning("No log files found in the selected output folder.")

if __name__ == "__main__":
    main()
