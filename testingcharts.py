import pandas as pd
import seaborn as sns

# Load the dataset
'''
data = {
    'gender': ['female', 'female', 'female', 'male', 'male', 'female', 'female', 'male', 'male', 'female', 'male', 'male', 'female', 'male', 'female', 'female', 'male', 'female', 'male', 'female', 'male', 'female', 'male', 'female', 'male'],
    'race_ethnicity': ['group B', 'group C', 'group B', 'group A', 'group C', 'group B', 'group B', 'group B', 'group D', 'group B', 'group B', 'group D', 'group B', 'group A', 'group A', 'group C', 'group C', 'group B', 'group C', 'group C', 'group D', 'group B', 'group D', 'group C', 'group D'],
    'parental_level_of_education': ["bachelor's degree", 'some college', "master's degree", "associate's degree", 'some college', "associate's degree", 'some college', 'high school', 'high school', 'high school', "associate's degree", "associate's degree", 'high school', 'some college', "master's degree", 'some high school', 'high school', 'some high school', "master's degree", "associate's degree", 'high school', 'some college', 'some college', 'some high school', "bachelor's degree"],
    'lunch': ['standard', 'standard', 'standard', 'free/reduced', 'standard', 'standard', 'standard', 'free/reduced', 'free/reduced', 'free/reduced', 'standard', 'standard', 'standard', 'standard', 'standard', 'standard', 'standard', 'free/reduced', 'free/reduced', 'free/reduced', 'standard', 'free/reduced', 'standard', 'standard', 'free/reduced'],
    'test_preparation_course': ['none', 'completed', 'none', 'none', 'none', 'none', 'completed', 'none', 'completed', 'none', 'none', 'none', 'none', 'completed', 'none', 'none', 'none', 'none', 'completed', 'none', 'none', 'completed', 'none', 'none', 'completed'],
    'math_score': [72, 69, 90, 47, 76, 71, 88, 40, 64, 38, 58, 40, 65, 78, 50, 69, 88, 18, 46, 54, 66, 65, 44, 69, 74],
    'reading_score': [72, 90, 95, 57, 78, 83, 95, 43, 64, 60, 54, 52, 81, 72, 53, 75, 89, 32, 42, 58, 69, 75, 54, 73, 71],
    'writing_score': [74, 88, 93, 44, 75, 78, 92, 39, 67, 50, 52, 43, 73, 70, 58, 78, 86, 28, 46, 61, 63, 70, 53, 73, 80]
}

df = pd.DataFrame(data)
'''

file_path = 'study_performance.csv'

# Load the dataset into a DataFrame
df = pd.read_csv(file_path)

import matplotlib.pyplot as plt

gender_counts = df['gender'].value_counts()
plt.figure(figsize=(8, 6))
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Gender Distribution')
plt.axis('equal')
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(x='parental_level_of_education', data=df, order=df['parental_level_of_education'].value_counts().index)
plt.title('Parental Level of Education')
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(16, 5))

plt.subplot(1, 3, 1)
sns.histplot(df['math_score'], bins=20, kde=True, color='blue')
plt.title('Math Score Distribution')

plt.subplot(1, 3, 2)
sns.histplot(df['reading_score'], bins=20, kde=True, color='green')
plt.title('Reading Score Distribution')

plt.subplot(1, 3, 3)
sns.histplot(df['writing_score'], bins=20, kde=True, color='red')
plt.title('Writing Score Distribution')

plt.tight_layout()
plt.show()

gender_scores = df.groupby('gender').mean()[['math_score', 'reading_score', 'writing_score']]
gender_scores.plot(kind='bar', figsize=(10, 6))
plt.title('Average Scores by Gender')
plt.ylabel('Average Score')
plt.xlabel('Gender')
plt.xticks(rotation=0)
plt.show()
