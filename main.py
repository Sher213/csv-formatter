import re
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.svm import SVC, SVR
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import os
import subprocess

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class DatasetScriptor:
    def __init__(self, dataset):
        """Initialize with the dataset file and OpenAI API key."""
        self.dataset_path = f"datasets/{dataset}"
        self.df = pd.read_csv(self.dataset_path)
        self.current_script_path = ""

    def get_command_from_openai(self, user_message):
        """Generate a Python command from OpenAI API based on user input."""
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"""You are an expert Python data scientist and analyst using pandas, 
                                                    scikitlearn, numpy and any other library a data scientist or analyst
                                                    might use. You can perform dataset cleaning, and analysis and machine 
                                                    learning models function and analysis. Ensure to load the csv from 
                                                    '{self.dataset_path}'. Here are the first 5 rows: \n\n
                                                    
                                                    {pd.read_csv(self.dataset_path).head()} \n\n
                                                    
                                                    Here is the dataset columns: {pd.read_csv(self.dataset_path).columns}.\n 
                                                    IMPORTANT: 1) Avoid any markings or explanantions and 2) just give the user the code. 
                                                    3) Do not include '```python'. 4) Call the dataset df."""},
                    {"role": "user", "content": user_message}
                ]
            )
            command = response.choices[0].message.content.strip()
            print(f"Generated command: {command}")
            return command
        except Exception as e:
            print(f"Error generating command: {e}")
            return None

    def save_command_to_script(self, command):
        """Save the generated command to a Python file in the scripts/ directory."""
        script_dir = "scripts"
        os.makedirs(script_dir, exist_ok=True)
        
        script_name = "generated_script.py"
        script_path = os.path.join(script_dir, script_name)
        
        script_content = f"""
# Execute the generated command
{command}

# Save the modified dataset
df.to_csv('{self.dataset_path}', index=False)
print('Dataset updated successfully.')
"""
        with open(script_path, "w", encoding="utf-8") as script_file:
            script_file.write(script_content)
        
        self.current_script_path = script_path
        print(f"Script saved to: {script_path}")

    def execute_script(self):
        """Execute the saved script using subprocess."""
        if not self.current_script_path:
            print("No script available. Please generate and save the script first.")
            return

        try:
            result = subprocess.run(["python", self.current_script_path], capture_output=True, text=True)
            if result.returncode == 0:
                print("Script executed successfully!")
                print(result.stdout)
            else:
                print(f"Error executing script: {result.stderr}")
        except Exception as e:
            print(f"Error running script: {e}")

    def run(self, user_message):
        """Main method to handle the entire flow: generate, save, and execute."""
        command = self.get_command_from_openai(user_message)
        if command:
            self.save_command_to_script(command)
            self.execute_script()