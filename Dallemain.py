from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import re

app = Flask(__name__)

def process_uploaded_file(file):
    """
    Process the uploaded file and return basic information about the dataset.
    """
    try:
        # Read the uploaded file
        if file.filename.endswith('.csv'):
            data = pd.read_csv(file)
        elif file.filename.endswith('.xls') or file.filename.endswith('.xlsx'):
            data = pd.read_excel(file)
        else:
            return "Unsupported file format. Please upload a CSV or Excel file."

        # Handle missing values
        missing_values = data.isnull().sum().sum()
        if missing_values > 0:
            data.dropna(inplace=True)

        # Handle outliers (example: replace outliers with median)
        numerical_columns = data.select_dtypes(include=np.number).columns
        for column in numerical_columns:
            q1 = data[column].quantile(0.25)
            q3 = data[column].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            data[column] = np.where(data[column] < lower_bound, data[column].median(), data[column])
            data[column] = np.where(data[column] > upper_bound, data[column].median(), data[column])

        # Format inconsistencies (example: convert date strings to datetime objects)
        # Add your format inconsistencies handling code here

        # Get basic information about the preprocessed dataset
        num_rows, num_cols = data.shape
        columns = data.columns.tolist()
        summary = data.describe().to_html()
        
        return {
            "num_rows": num_rows,
            "num_cols": num_cols,
            "columns": columns,
            "summary": summary
        }
    except Exception as e:
        return f"Error processing file: {e}"

def process_user_query(query, data):
    """
    Process user query and return relevant information or visualization.
    """
    # Define regular expressions to match common data analysis queries
    query_patterns = {
        r'.*(rows|observations).*': lambda: f"Number of rows: {data.shape[0]}",
        r'.*(columns|variables|features).*': lambda: f"Number of columns: {data.shape[1]}",
        r'.*summary.*': lambda: data.describe().to_html(),
        # Add more patterns as needed for other queries
    }

    # Match query patterns and execute corresponding functions
    for pattern, func in query_patterns.items():
        if re.match(pattern, query, re.IGNORECASE):
            return func()

    # If no match found, return error message
    return "Sorry, I didn't understand your query."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return render_template('index.html', error="No file uploaded.")
        
        file = request.files['file']

        # Check if file is uploaded
        if file.filename == '':
            return render_template('index.html', error="No file selected.")

        # Process the uploaded file
        result = process_uploaded_file(file)
        if isinstance(result, str):
            return render_template('index.html', error=result)
        else:
            return render_template('index.html', result=result)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
