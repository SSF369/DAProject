import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming your dataset is named 'dataset.csv', adjust the file path as needed
file_path = 'study_performance.csv'

# Load the dataset into a DataFrame
df = pd.read_csv(file_path)

# Display basic information about the dataset
print("Dataset shape:", df.shape)
print("Columns:", df.columns)
print("Descriptive Statistics:\n", df.describe())

# Visualize gender distribution
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='gender')
plt.title('Gender Distribution')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.show()

# Visualize race/ethnicity distribution
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='race_ethnicity', order=df['race_ethnicity'].value_counts().index)
plt.title('Race/Ethnicity Distribution')
plt.xlabel('Race/Ethnicity')
plt.ylabel('Count')
plt.show()

# Visualize parental level of education distribution
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='parental_level_of_education', order=df['parental_level_of_education'].value_counts().index)
plt.title('Parental Level of Education Distribution')
plt.xlabel('Parental Level of Education')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

# Visualize lunch type distribution
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='lunch')
plt.title('Lunch Type Distribution')
plt.xlabel('Lunch Type')
plt.ylabel('Count')
plt.show()

# Visualize test preparation course distribution
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='test_preparation_course')
plt.title('Test Preparation Course Distribution')
plt.xlabel('Test Preparation Course')
plt.ylabel('Count')
plt.show()

# Visualize scores distribution
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='math_score', bins=20, kde=True, label='Math Score')
sns.histplot(data=df, x='reading_score', bins=20, kde=True, label='Reading Score')
sns.histplot(data=df, x='writing_score', bins=20, kde=True, label='Writing Score')
plt.title('Scores Distribution')
plt.xlabel('Score')
plt.ylabel('Count')
plt.legend()
plt.show()
