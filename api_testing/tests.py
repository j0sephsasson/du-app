import unittest
import api
import requests
import json
from unittest.mock import patch, Mock

class APITestCases(unittest.TestCase):
    """
    Test case class for API functionalities.

    Attributes:
    - file_path (str): File path used for testing.
    - text (str): Text used for testing.
    - fields (str): Fields used for testing.
    """

    def __init__(self, methodName='runTest', file_path=None, text=None, fields=None):
        """
        Initialize the APITestCases with required attributes.

        Parameters:
        - methodName (str): Name of the method to be run. Defaults to 'runTest'.
        - file_path (str, required): Path to the file for testing.
        - text (str, required): Text input for testing.
        - fields (str, required): Fields input for testing.
        """
        super(APITestCases, self).__init__(methodName)
        self.file_path = file_path or "some_default_path.pdf"
        self.text = text or "Some default text"
        self.fields = fields or "Default fields"

    @patch('api.requests.post')
    def test_send_to_ocr_api_success(self, mock_post):
        """
        Test the success scenario of sending a file to the OCR API.
        """
        mock_response = Mock()
        mock_response.json.return_value = {'ocr_result': 'Test OCR result'}
        mock_post.return_value = mock_response

        result = api.send_to_ocr_api(self.file_path)
        self.assertEqual(result, {'ocr_result': 'Test OCR result'})

    @patch('api.requests.post')
    def test_send_to_ocr_api_failure_non_json_response(self, mock_post):
        """
        Test the failure scenario when the OCR API responds with a non-JSON response.
        """
        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("", "", 0)
        mock_post.return_value = mock_response

        with self.assertRaises(ValueError):
            api.send_to_ocr_api(self.file_path)

    @patch('api.requests.post')
    def test_send_to_ocr_api_failure_http_error(self, mock_post):
        """
        Test the failure scenario when the OCR API responds with an HTTP error.
        """
        mock_post.side_effect = requests.HTTPError()

        with self.assertRaises(ValueError):
            api.send_to_ocr_api(self.file_path)

    @patch('api.requests.post')
    def test_send_to_ocr_api_failure_timeout(self, mock_post):
        """
        Test the failure scenario when there's a timeout while calling the OCR API.
        """
        mock_post.side_effect = requests.Timeout()

        with self.assertRaises(ValueError):
            api.send_to_ocr_api(self.file_path)

    @patch('api.requests.post')
    def test_send_to_ocr_api_failure_connection_error(self, mock_post):
        """
        Test the failure scenario when there's a connection error while calling the OCR API.
        """
        mock_post.side_effect = requests.ConnectionError()

        with self.assertRaises(ValueError):
            api.send_to_ocr_api(self.file_path)

    @patch('api.requests.post')
    def test_send_to_llm_api_success(self, mock_post):
        """
        Test the success scenario of sending data to the LLM API.
        """
        mock_response = Mock()
        mock_response.json.return_value = {'result': 'Test LLM result'}
        mock_post.return_value = mock_response

        result = api.send_to_llm_api(self.text, self.fields)
        self.assertEqual(result, {'result': 'Test LLM result'})

    @patch('api.requests.post')
    def test_send_to_llm_api_failure_non_json_response(self, mock_post):
        """
        Test the failure scenario when the LLM API responds with a non-JSON response.
        """
        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("", "", 0)
        mock_post.return_value = mock_response

        with self.assertRaises(ValueError):
            api.send_to_llm_api(self.text, self.fields)

    @patch('api.requests.post')
    def test_send_to_llm_api_failure_http_error(self, mock_post):
        """
        Test the failure scenario when the LLM API responds with an HTTP error.
        """
        mock_post.side_effect = requests.HTTPError()

        with self.assertRaises(ValueError):
            api.send_to_llm_api(self.text, self.fields)

    @patch('api.requests.post')
    def test_send_to_llm_api_failure_timeout(self, mock_post):
        """
        Test the failure scenario when there's a timeout while calling the LLM API.
        """
        mock_post.side_effect = requests.Timeout()

        with self.assertRaises(ValueError):
            api.send_to_llm_api(self.text, self.fields)

    @patch('api.requests.post')
    def test_send_to_llm_api_failure_connection_error(self, mock_post):
        """
        Test the failure scenario when there's a connection error while calling the LLM API.
        """
        mock_post.side_effect = requests.ConnectionError()

        with self.assertRaises(ValueError):
            api.send_to_llm_api(self.text, self.fields)

if __name__ == '__main__':
    unittest.main()