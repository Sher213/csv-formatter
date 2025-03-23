from flask import Flask, render_template, request, jsonify, send_file
import os
from main import DatasetScriptor
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'datasets'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure required directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('scripts', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.csv'):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename})
    
    return jsonify({'error': 'Invalid file type. Please upload a CSV file.'}), 400

@app.route('/process', methods=['POST'])
def process_dataset():
    data = request.json
    dataset_name = data.get('dataset')
    user_message = data.get('message')
    
    if not dataset_name or not user_message:
        return jsonify({'error': 'Missing dataset name or message'}), 400
    
    try:
        scriptor = DatasetScriptor(dataset_name)
        scriptor.run(user_message)
        return jsonify({'message': 'Dataset processed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            as_attachment=True
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/preview/<filename>')
def preview_dataset(filename):
    try:
        df = pd.read_csv(f"datasets/{filename}")
        # Convert DataFrame to JSON format
        preview_data = {
            'headers': df.columns.tolist(),
            'rows': df.head(5).values.tolist()
        }
        return jsonify(preview_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) 