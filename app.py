from flask import Flask, render_template, jsonify, request
from data_processor import DataProcessor
import json
import os


app = Flask(__name__)


# Initialize processor
processor = DataProcessor()

# Create necessary directories
os.makedirs('output', exist_ok=True)
os.makedirs('uploads', exist_ok=True)

# Load results
def load_results():
    try:
        with open('output/classifications.json', 'r') as f:
            classifications = json.load(f)
        with open('output/tasks.json', 'r') as f:
            tasks = json.load(f)
        with open('output/sensitive.json', 'r') as f:
            sensitive = json.load(f)
        with open('output/statistics.json', 'r') as f:
            statistics = json.load(f)
        return classifications, tasks, sensitive, statistics
    except FileNotFoundError:
        return [], {'tasks': [], 'events': []}, [], {'total': 0, 'categories': {}, 'sensitive_count': 0, 'tasks_count': 0, 'events_count': 0}
    except:
        return [], {'tasks': [], 'events': []}, [], {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/classifications')
def get_classifications():
    classifications, _, _, _ = load_results()
    return jsonify(classifications)

@app.route('/api/tasks')
def get_tasks():
    _, tasks, _, _ = load_results()
    return jsonify(tasks)

@app.route('/api/sensitive')
def get_sensitive():
    _, _, sensitive, _ = load_results()
    return jsonify(sensitive)

@app.route('/api/statistics')
def get_statistics():
    _, _, _, statistics = load_results()
    return jsonify(statistics)

@app.route('/api/mandatory/<message_id>')
def get_mandatory(message_id):
    classifications, _, _, _ = load_results()
    for item in classifications:
        if item['message_id'] == message_id:
            return jsonify(item)
    return jsonify({'error': 'Message not found'}), 404

@app.route('/api/process', methods=['POST'])
def process_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save uploaded file
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    
    # Process
    results = processor.process_messages(file_path)
    return jsonify({'success': True, 'statistics': results['statistics']})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
