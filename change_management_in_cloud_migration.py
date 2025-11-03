# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set visualization style
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ----------------------------
# Step 1: Load Dataset
# ----------------------------
# Replace 'cloud_issues.csv' with your dataset file from Kaggle
df = pd.read_csv('cloud_issues.csv')

# Display basic info
print("Dataset Info:")
print(df.info())
print("\nFirst 5 rows:")
print(df.head())

# ----------------------------
# Step 2: Data Preprocessing
# ----------------------------
# Convert date columns to datetime
df['Reported_Date'] = pd.to_datetime(df['Reported_Date'], errors='coerce')
df['Resolved_Date'] = pd.to_datetime(df['Resolved_Date'], errors='coerce')

# Fill missing values if any
df['Issue_Type'] = df['Issue_Type'].fillna('Unknown')
df['Severity'] = df['Severity'].fillna('Medium')
df['Resolution_Status'] = df['Resolution_Status'].fillna('Open')

# Calculate resolution time in days
df['Resolution_Time_Days'] = (df['Resolved_Date'] - df['Reported_Date']).dt.days

# ----------------------------
# Step 3: Basic Analysis
# ----------------------------
print("\nNumber of issues per type:")
print(df['Issue_Type'].value_counts())

print("\nNumber of issues by severity:")
print(df['Severity'].value_counts())

print("\nAverage resolution time by severity:")
print(df.groupby('Severity')['Resolution_Time_Days'].mean())

# ----------------------------
# Step 4: Visualization
# ----------------------------

# 4a: Issue Type Distribution
plt.figure()
sns.countplot(y='Issue_Type', data=df, order=df['Issue_Type'].value_counts().index, palette='Set2')
plt.title('Distribution of Issues by Type')
plt.xlabel('Count')
plt.ylabel('Issue Type')
plt.show()

# 4b: Severity Distribution
plt.figure()
sns.countplot(x='Severity', data=df, palette='Set1')
plt.title('Distribution of Issues by Severity')
plt.xlabel('Severity')
plt.ylabel('Count')
plt.show()

# 4c: Resolution Time by Severity
plt.figure()
sns.boxplot(x='Severity', y='Resolution_Time_Days', data=df, palette='Set3')
plt.title('Resolution Time by Severity')
plt.xlabel('Severity')
plt.ylabel('Resolution Time (Days)')
plt.show()

# 4d: Issues Over Time
issues_over_time = df.groupby(df['Reported_Date'].dt.to_period('M')).size()
issues_over_time.index = issues_over_time.index.to_timestamp()
plt.figure()
issues_over_time.plot(marker='o')
plt.title('Number of Issues Reported Over Time')
plt.xlabel('Month')
plt.ylabel('Number of Issues')
plt.show()

# 4e: Resolution Status Pie Chart
status_counts = df['Resolution_Status'].value_counts()
plt.figure()
plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title('Issue Resolution Status')
plt.show()

# ----------------------------
# Step 5: Insights
# ----------------------------
# Identify top recurring issues
top_issues = df['Issue_Type'].value_counts().head(5)
print("\nTop 5 Recurring Issues:")
print(top_issues)

# Identify issues with longest resolution times
longest_issues = df[['Issue_ID','Issue_Type','Resolution_Time_Days']].sort_values(by='Resolution_Time_Days', ascending=False).head(5)
print("\nTop 5 Issues with Longest Resolution Time:")
print(longest_issues)
