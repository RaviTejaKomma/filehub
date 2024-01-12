import unittest
from io import BytesIO
from api import create_app
import requests


class TestFileHub(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.uploaded_test_file_id = None

    def test_health_check_endpoint(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(True), 'Hey there! Welcome to FileHub.')

    def test_upload_file(self):
        data = {
            'file': (BytesIO(b'test content'), 'test_file.txt'),
            'file_name': 'Test File'
        }
        response = self.app.post('/api/v1/files/upload', data=data, content_type='multipart/form-data')
        # Parse the response JSON
        response_json = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_json['status'])
        self.assertEqual(response_json['data']['file_name'], 'Test File')
        self.assertEqual(response_json['data']['file_ext'], 'txt')

        # Store the file_id for subsequent tests #
        self.uploaded_test_file_id = response_json['data']['_id']

    def test_read_file(self):
        response = self.app.get(f'/api/v1/files/{self.uploaded_test_file_id}')
        response_json = response.get_json()
        self.assertEqual(response.status_code, 200)

    def test_list_files(self):
        response = self.app.get('/api/v1/files/')
        response_json = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_json['status'])

    def test_update_file(self):
        # Test update file API #
        pass

    def test_delete_file(self):
        # Test delete file API #
        pass


if __name__ == '__main__':
    unittest.main()
