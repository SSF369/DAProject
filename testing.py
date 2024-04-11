from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns

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

        # Get basic information about the preprocessed dataset
        num_rows, num_cols = data.shape
        columns = data.columns.tolist()
        summary = data.describe().to_html()
        
        return {
            "num_rows": num_rows,
            "num_cols": num_cols,
            "columns": columns,
            "summary": summary,
            "data": data  # Include preprocessed data
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

def generate_correlation_insights(data):
    """
    Generate insights based on correlations and relationships between columns.
    """
    insights = []

    # Analyze relationships between columns
    for column in data.columns:
        if data[column].dtype == 'object':
            # For categorical columns, provide value counts
            value_counts = data[column].value_counts().to_dict()
            insights.append(f"Column '{column}' contains the following categories: {', '.join([f'{category}: {count}' for category, count in value_counts.items()])}")
        elif data[column].dtype in ['int64', 'float64']:
            # For numerical columns, calculate mean, median, and standard deviation
            mean = data[column].mean()
            median = data[column].median()
            std_dev = data[column].std()
            insights.append(f"For column '{column}', mean is {mean:.2f}, median is {median:.2f}, and standard deviation is {std_dev:.2f}")

    return insights


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
            # Generate descriptive statistics
            descriptive_stats = result['data'].describe().to_html()

            # Summarize key aspects of the dataset
            data_summary = f"Dataset contains {result['num_rows']} rows and {result['num_cols']} columns. Columns: {', '.join(result['columns'])}."

            # Generate potential information about the dataset
            potential_info = generate_correlation_insights(result['data'])

            # Generate insights based on correlations between numerical columns
            correlation_insights = generate_correlation_insights(result['data'])

            # Data Visualization: Generate some sample visualizations
            # Example: Pairplot for visualizing relationships between numerical variables
            plt.figure(figsize=(10, 8))
            sns.pairplot(result['data'])
            plt.title('Pairplot of Numerical Variables')
            plt.xlabel('Numerical Variables')
            plt.ylabel('Numerical Variables')
            plt.savefig('static/pairplot.png')  # Save the visualization as a static file
            plt.close()

            # Render the template with results
            return render_template('index.html', result=result, descriptive_stats=descriptive_stats,
                                    data_summary=data_summary, potential_info=potential_info,
                                    correlation_insights=correlation_insights)

    return render_template('index.html')

@app.route('/download')
def download():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
