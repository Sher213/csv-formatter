import re
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
import numpy as np
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class DatasetScriptor:
    def __init__(self, dataset):
        """Initialize with the dataset file and OpenAI API key."""
        self.dataset_path = f"/tmp/datasets/{dataset}"
        self.df = pd.read_csv(self.dataset_path)
        self.current_script_path = ""

    def get_command_from_openai(self, user_message):
        """Generate a Python command from OpenAI API based on user input."""
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"""You are an expert Python data analyst using pandas and numpy.
                                                    You can perform dataset cleaning, basic analysis, and transformations.
                                                    Ensure to load the csv from '{self.dataset_path}'. 
                                                    Here are the first 5 rows: \n\n
                                                    
                                                    {pd.read_csv(self.dataset_path).head()} \n\n
                                                    
                                                    Here is the dataset columns: {pd.read_csv(self.dataset_path).columns}.\n 
                                                    IMPORTANT: 1) Avoid any markings or explanations and 2) just give the user the code. 
                                                    3) Do not include '```python'. 4) Call the dataset df.
                                                    5) Only use pandas and numpy operations."""},
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
        script_dir = "/tmp/scripts"
        os.makedirs(script_dir, exist_ok=True)
        
        script_name = "generated_script.py"
        script_path = os.path.join(script_dir, script_name)
        
        script_content = f"""
import pandas as pd
import numpy as np

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
        """Execute the saved script."""
        if not self.current_script_path:
            print("No script available. Please generate and save the script first.")
            return

        try:
            with open(self.current_script_path, 'r') as f:
                script_content = f.read()
            exec(script_content)
            print("Script executed successfully!")
        except Exception as e:
            print(f"Error running script: {e}")

    def run(self, user_message):
        """Main method to handle the entire flow: generate, save, and execute."""
        command = self.get_command_from_openai(user_message)
        if command:
            self.save_command_to_script(command)
            self.execute_script()