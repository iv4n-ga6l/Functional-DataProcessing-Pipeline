from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from config import FileFormat, PipelineConfig, config
from pipeline import DataPipeline
import json
from waitress import serve
from pycache_handler.handler import py_cache_handler


app = Flask(__name__)
app.config['DEBUG'] = config[os.getenv('FLASK_ENV', 'development')]
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'csv', 'json', 'xlsx', 'parquet'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def parse_and_validate_json_object(field_name: str, raw_value: str) -> dict:
    """Parse a JSON string and validate it is a non-null object (dict).

    Args:
        field_name: Human-readable name used in error messages.
        raw_value: Raw JSON string from the request form.

    Returns:
        The parsed dict.

    Raises:
        ValueError: If the value is not valid JSON or not a JSON object.
    """
    try:
        parsed = json.loads(raw_value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"'{field_name}' contains invalid JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError(
            f"'{field_name}' must be a JSON object (got {type(parsed).__name__})"
        )
    return parsed


def validate_column_mappings(mappings: dict) -> None:
    """Validate that column_mappings contains only string values.

    JSON object keys are always strings when parsed by json.loads(), so only
    the values need to be checked.

    Raises:
        ValueError: If any value is not a string.
    """
    for key, value in mappings.items():
        if not isinstance(value, str):
            raise ValueError(
                f"'column_mappings' values must be strings (got {type(value).__name__} for key '{key}')"
            )


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

        # Get and validate form data
        input_format = request.form.get('input_format')
        output_format = request.form.get('output_format')

        if not input_format:
            return jsonify({'error': 'input_format is required'}), 400
        if not output_format:
            return jsonify({'error': 'output_format is required'}), 400

        valid_formats = {f.value for f in FileFormat}
        if input_format not in valid_formats:
            return jsonify({'error': f"Invalid input_format '{input_format}'. Must be one of: {sorted(valid_formats)}"}), 400
        if output_format not in valid_formats:
            return jsonify({'error': f"Invalid output_format '{output_format}'. Must be one of: {sorted(valid_formats)}"}), 400

        raw_batch_size = request.form.get('batch_size', '1000')
        try:
            batch_size = int(raw_batch_size)
            if batch_size < 1:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({'error': 'batch_size must be a positive integer'}), 400

        required_columns = request.form.get('required_columns', '').split(',') if request.form.get('required_columns') else []

        raw_column_mappings = request.form.get('column_mappings', '').strip()
        if raw_column_mappings:
            try:
                column_mappings = parse_and_validate_json_object('column_mappings', raw_column_mappings)
                validate_column_mappings(column_mappings)
            except ValueError as exc:
                return jsonify({'error': exc.args[0]}), 400
        else:
            column_mappings = {}

        raw_filter_conditions = request.form.get('filter_conditions', '').strip()
        if raw_filter_conditions:
            try:
                filter_conditions = parse_and_validate_json_object('filter_conditions', raw_filter_conditions)
            except ValueError as exc:
                return jsonify({'error': exc.args[0]}), 400
        else:
            filter_conditions = {}

        # Create output filename
        output_filename = f"processed_data.{output_format.lower()}" if output_format != "excel" else "processed_data.xlsx"
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
