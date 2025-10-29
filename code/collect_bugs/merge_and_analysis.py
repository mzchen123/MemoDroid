import pandas as pd

# Read CSV files
closed_issues = pd.read_csv('issues_closed.csv')
open_issues = pd.read_csv('issues_open.csv')

# Merge data
merged_data = pd.concat([closed_issues, open_issues], ignore_index=True)

# Filter data for specified categories
target_categories = ['money', 'multimedia', 'reading']
filtered_data = merged_data[merged_data['Category'].isin(target_categories)]

# Count the number of occurrences for each app
app_counts = filtered_data['App Name'].value_counts().reset_index()
app_counts.columns = ['App Name', 'Count']

# Merge count data back into the original data
filtered_data = filtered_data.merge(app_counts, on='App Name')

# Sort by count
filtered_data = filtered_data.sort_values('Count', ascending=False)

# Keep only the required columns
result_data = filtered_data[['Category', 'App Name', 'Github Link', 'F-Droid Link']]

# Remove duplicate rows
result_data = result_data.drop_duplicates()

# Group by category and save results
for category in target_categories:
    category_data = result_data[result_data['Category'] == category]
    output_file = f'filtered_apps_{category}.csv'
    category_data.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Processing for category {category} completed! Results saved to {output_file}")

# Save the complete result
result_data.to_csv('filtered_apps_all.csv', index=False, encoding='utf-8-sig')
print("Complete results for all categories have been saved to filtered_apps_all.csv")
