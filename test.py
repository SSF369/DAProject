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
    Perform basic analysis on the data and provide insights.
    
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
        
        # Provide insights about the data
        print("\nInsights:")
        for column in data.columns:
            unique_values = data[column].unique()
            num_unique_values = len(unique_values)
            print("- Column '{}':".format(column))
            print("  - Number of unique values:", num_unique_values)
            if num_unique_values <= 10:
                print("  - Unique values:", unique_values)
            print()  # Add a newline for readability
        
        # Return column names for further analysis
        return data.columns.tolist()
    except Exception as e:
        print("Error performing basic analysis:", e)
        return None

def generate_charts(data):
    """
    Automatically generate different types of charts based on the data.
    
    Parameters:
    - data (DataFrame): DataFrame containing the input data.
    """
    try:
        chart_types = set()  # Set to store generated chart types
        
        plt.figure(figsize=(10, 8))  # Set figure size for better visibility
        
        # Generate bar charts for categorical columns
        categorical_columns = data.select_dtypes(include=['object', 'category']).columns
        for column in categorical_columns:
            if 'bar' not in chart_types:
                plt.figure(figsize=(8, 6))
                data[column].value_counts().plot(kind='bar', color='skyblue')
                plt.xlabel(column)
                plt.ylabel('Count')
                plt.title('Bar Chart: {}'.format(column))
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
                chart_types.add('bar')
        
        # Generate histogram for numerical columns
        numerical_columns = data.select_dtypes(include=['int', 'float']).columns
        for column in numerical_columns:
            if 'hist' not in chart_types:
                plt.figure(figsize=(8, 6))
                data[column].plot(kind='hist', color='salmon', bins=20)
                plt.xlabel(column)
                plt.ylabel('Frequency')
                plt.title('Histogram: {}'.format(column))
                plt.tight_layout()
                plt.show()
                chart_types.add('hist')
        
        # Generate scatter plot for pairs of numerical columns
        for i in range(len(numerical_columns)):
            for j in range(i + 1, len(numerical_columns)):
                if 'scatter' not in chart_types:
                    plt.figure(figsize=(8, 6))
                    plt.scatter(data[numerical_columns[i]], data[numerical_columns[j]], color='orange')
                    plt.xlabel(numerical_columns[i])
                    plt.ylabel(numerical_columns[j])
                    plt.title('Scatter Plot: {} vs {}'.format(numerical_columns[j], numerical_columns[i]))
                    plt.tight_layout()
                    plt.show()
                    chart_types.add('scatter')
        
    except Exception as e:
        print("Error generating charts:", e)

# Allow user to provide file path as input
file_path = input("Enter the path to the CSV or Excel file: ")

# Read data from file
data = read_data(file_path)
if data is not None:
    # Perform basic analysis and provide insights
    columns = basic_analysis(data)
    if columns is not None:
        # Generate charts automatically
        generate_charts(data)
