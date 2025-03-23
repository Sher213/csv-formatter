
# Execute the generated command
import pandas as pd

df = pd.read_csv('datasets/BabyWeightSmoking.csv')

# Conversion factor from kilograms to pounds
kg_to_lb = 2.20462

df['BirthWeightLB'] = df['BirthWeight'] * kg_to_lb

# Save the modified dataset
df.to_csv('datasets/BabyWeightSmoking.csv', index=False)
print('Dataset updated successfully.')
