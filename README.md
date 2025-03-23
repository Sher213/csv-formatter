# Dataset Formatter Web App

A web application that allows users to upload, process, and format CSV datasets using natural language instructions powered by OpenAI's GPT-4.

## Features

- Upload CSV datasets
- Process datasets using natural language instructions
- Download processed datasets
- Modern, responsive UI built with Tailwind CSS
- Secure file handling and processing

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd dataset-formatter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Upload a CSV file using the "Choose CSV File" button
2. Enter the dataset name and processing instructions
3. Click "Process Dataset" to apply the changes
4. Download the processed dataset using the "Download Processed Dataset" button

## Project Structure

- `app.py`: Main Flask application
- `main.py`: Dataset processing logic
- `templates/index.html`: Web interface
- `datasets/`: Directory for uploaded CSV files
- `scripts/`: Directory for generated processing scripts

## Security Notes

- The application has a 16MB file size limit
- Only CSV files are accepted
- All file operations are performed in secure directories
- API keys are stored in environment variables

## License

MIT License 