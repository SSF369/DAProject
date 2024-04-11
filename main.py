import pandas as pd
import matplotlib.pyplot as plt

def read_data(file_path):
    """
    Read data from a CSV or Excel file.
    
    Parameters:
    - file_path (str): Path to the input file.
    
    Returns:
    - data (DataFrame): DataFrame containing the data from the file.
    """
    try:
        # Read data from CSV or Excel file
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
        
        return data
    except Exception as e:
        print("Error reading data:", e)
        return None

def basic_analysis(data):
    """
    Perform basic analysis on the data.
    
    Parameters:
    - data (DataFrame): DataFrame containing the input data.
    
    Returns:
    - columns (list): List of column names in the data.
    """
    try:
        # Display summary statistics
        summary_stats = data.describe()
        print("Summary Statistics:")
        print(summary_stats)
        
        # Display data types of columns
        data_types = data.dtypes
        print("\nData Types:")
        print(data_types)
        
        # Return column names for further analysis
        return data.columns.tolist()
    except Exception as e:
        print("Error performing basic analysis:", e)
        return None

def generate_chart(data, x_column, y_column, chart_type):
    """
    Generate a chart based on user input.
    
    Parameters:
    - data (DataFrame): DataFrame containing the input data.
    - x_column (str): Name of the column for the x-axis.
    - y_column (str): Name of the column for the y-axis.
    - chart_type (str): Type of chart to generate ('bar' or 'line').
    """
    try:
        if chart_type == 'bar':
            plt.bar(data[x_column], data[y_column])
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.title("Bar Chart: {} vs {}".format(x_column, y_column))
        elif chart_type == 'line':
            plt.plot(data[x_column], data[y_column])
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.title("Line Plot: {} vs {}".format(x_column, y_column))
        else:
            raise ValueError("Unsupported chart type. Please select 'bar' or 'line'.")
        
        plt.show()
    except Exception as e:
        print("Error generating chart:", e)

# Allow user to provide file path as input
file_path = input("Enter the path to the CSV or Excel file: ")

# Read data from file
data = read_data(file_path)
if data is not None:
    # Perform basic analysis
    columns = basic_analysis(data)
    if columns is not None and len(columns) >= 2:
        # Example usage: Generate a chart
        x_column = columns[0]  # Using the first column as x-axis
        y_column = columns[1]  # Using the second column as y-axis
        chart_type = 'bar'     # Example chart type (can be 'bar' or 'line')
        generate_chart(data, x_column, y_column, chart_type)
