from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from config import FileFormat, PipelineConfig, config
from pipeline import DataPipeline
import json
from waitress import serve
from pycache_handler.handler import py_cache_handler


app = Flask(__name__)
app.config.from_object(config[os.getenv('FLASK_ENV', 'development')])
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'csv', 'json', 'xlsx', 'parquet'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', file_formats=[format.value for format in FileFormat])

@app.route('/process', methods=['POST'])
def process_data():
    try:
        # Handle file upload
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format'}), 400

        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        # Get form data
        input_format = request.form.get('input_format')
        output_format = request.form.get('output_format')
        batch_size = int(request.form.get('batch_size', 1000))
        required_columns = request.form.get('required_columns', '').split(',') if request.form.get('required_columns') else []
        column_mappings = json.loads(request.form.get('column_mappings', '{}')) if request.form.get('column_mappings') else {}
        filter_conditions = json.loads(request.form.get('filter_conditions', '{}')) if request.form.get('filter_conditions') else {}
        
        # Create output filename
        output_filename = f"processed_data.{output_format.lower()}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

        # Configure and run pipeline
        config = PipelineConfig(
            input_path=input_path,
            output_path=output_path,
            input_format=FileFormat(input_format),
            output_format=FileFormat(output_format),
            batch_size=batch_size,
            required_columns=required_columns,
            column_mappings=column_mappings,
            filter_conditions=filter_conditions
        )
        
        pipeline = DataPipeline(config)
        pipeline.process()

        return send_file(
            output_path,
            as_attachment=True,
            download_name=output_filename
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@py_cache_handler
def main():
    if app.config['DEBUG']:
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        serve(app, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
