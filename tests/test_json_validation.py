import pytest
import sys
import os
import io

# Ensure the project root is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app, parse_and_validate_json_object, validate_column_mappings


# ---------------------------------------------------------------------------
# Unit tests for parse_and_validate_json_object
# ---------------------------------------------------------------------------

class TestParseAndValidateJsonObject:
    def test_valid_object(self):
        result = parse_and_validate_json_object('test_field', '{"a": "b"}')
        assert result == {"a": "b"}

    def test_empty_object(self):
        result = parse_and_validate_json_object('test_field', '{}')
        assert result == {}

    def test_invalid_json_raises(self):
        with pytest.raises(ValueError, match="contains invalid JSON"):
            parse_and_validate_json_object('test_field', '{not valid json}')

    def test_json_array_raises(self):
        with pytest.raises(ValueError, match="must be a JSON object"):
            parse_and_validate_json_object('test_field', '[1, 2, 3]')

    def test_json_string_raises(self):
        with pytest.raises(ValueError, match="must be a JSON object"):
            parse_and_validate_json_object('test_field', '"just a string"')

    def test_json_number_raises(self):
        with pytest.raises(ValueError, match="must be a JSON object"):
            parse_and_validate_json_object('test_field', '42')

    def test_json_null_raises(self):
        with pytest.raises(ValueError, match="must be a JSON object"):
            parse_and_validate_json_object('test_field', 'null')

    def test_field_name_in_error_message(self):
        with pytest.raises(ValueError, match="'my_special_field'"):
            parse_and_validate_json_object('my_special_field', '[1]')


# ---------------------------------------------------------------------------
# Unit tests for validate_column_mappings
# ---------------------------------------------------------------------------

class TestValidateColumnMappings:
    def test_valid_mappings(self):
        # Should not raise
        validate_column_mappings({"old_name": "new_name", "col_a": "col_b"})

    def test_empty_mappings(self):
        # Should not raise
        validate_column_mappings({})

    def test_non_string_value_raises(self):
        with pytest.raises(ValueError, match="values must be strings"):
            validate_column_mappings({"col": 123})

    def test_non_string_value_none_raises(self):
        with pytest.raises(ValueError, match="values must be strings"):
            validate_column_mappings({"col": None})


# ---------------------------------------------------------------------------
# Integration tests via Flask test client
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def _make_form_data(extra=None):
    """Build a minimal multipart form data dict with a small CSV file."""
    data = {
        'file': (io.BytesIO(b"name,age\nAlice,30\n"), 'data.csv'),
        'input_format': 'csv',
        'output_format': 'csv',
        'batch_size': '100',
    }
    if extra:
        data.update(extra)
    return data


class TestProcessEndpointJsonValidation:
    def test_invalid_column_mappings_json(self, client):
        data = _make_form_data({'column_mappings': '{bad json'})
        response = client.post('/process', data=data, content_type='multipart/form-data')
        assert response.status_code == 400
        body = response.get_json()
        assert 'column_mappings' in body['error']

    def test_column_mappings_is_array(self, client):
        data = _make_form_data({'column_mappings': '[1, 2]'})
        response = client.post('/process', data=data, content_type='multipart/form-data')
        assert response.status_code == 400
        body = response.get_json()
        assert 'column_mappings' in body['error']

    def test_column_mappings_non_string_value(self, client):
        data = _make_form_data({'column_mappings': '{"col": 42}'})
        response = client.post('/process', data=data, content_type='multipart/form-data')
        assert response.status_code == 400
        body = response.get_json()
        assert 'column_mappings' in body['error']

    def test_invalid_filter_conditions_json(self, client):
        data = _make_form_data({'filter_conditions': '{bad json'})
        response = client.post('/process', data=data, content_type='multipart/form-data')
        assert response.status_code == 400
        body = response.get_json()
        assert 'filter_conditions' in body['error']

    def test_filter_conditions_is_array(self, client):
        data = _make_form_data({'filter_conditions': '[1, 2]'})
        response = client.post('/process', data=data, content_type='multipart/form-data')
        assert response.status_code == 400
        body = response.get_json()
        assert 'filter_conditions' in body['error']

    def test_invalid_batch_size_zero(self, client):
        data = _make_form_data({'batch_size': '0'})
        response = client.post('/process', data=data, content_type='multipart/form-data')
        assert response.status_code == 400
        body = response.get_json()
        assert 'batch_size' in body['error']

    def test_invalid_batch_size_negative(self, client):
        data = _make_form_data({'batch_size': '-5'})
        response = client.post('/process', data=data, content_type='multipart/form-data')
        assert response.status_code == 400
        body = response.get_json()
        assert 'batch_size' in body['error']

    def test_invalid_batch_size_non_numeric(self, client):
        data = _make_form_data({'batch_size': 'abc'})
        response = client.post('/process', data=data, content_type='multipart/form-data')
        assert response.status_code == 400
        body = response.get_json()
        assert 'batch_size' in body['error']

    def test_invalid_input_format(self, client):
        data = _make_form_data({'input_format': 'xml'})
        response = client.post('/process', data=data, content_type='multipart/form-data')
        assert response.status_code == 400
        body = response.get_json()
        assert 'input_format' in body['error']

    def test_invalid_output_format(self, client):
        data = _make_form_data({'output_format': 'xml'})
        response = client.post('/process', data=data, content_type='multipart/form-data')
        assert response.status_code == 400
        body = response.get_json()
        assert 'output_format' in body['error']

    def test_missing_input_format(self, client):
        data = _make_form_data()
        del data['input_format']
        response = client.post('/process', data=data, content_type='multipart/form-data')
        assert response.status_code == 400
        body = response.get_json()
        assert 'input_format' in body['error']

    def test_missing_output_format(self, client):
        data = _make_form_data()
        del data['output_format']
        response = client.post('/process', data=data, content_type='multipart/form-data')
        assert response.status_code == 400
        body = response.get_json()
        assert 'output_format' in body['error']
