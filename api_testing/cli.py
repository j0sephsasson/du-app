import argparse
from tests import APITestCases
import unittest

def main():
    """
    Command-line tool to test OCR and LLM APIs using given arguments.
    """
    parser = argparse.ArgumentParser(description="API Test Tool")

    # Common arguments
    parser.add_argument('--action', type=str, choices=['ocr', 'llm'], required=True, help="Choose between 'ocr' or 'llm'")
    parser.add_argument('--file_path', type=str, help="Path to the file for testing OCR API.")
    parser.add_argument('--text', type=str, help="Text input for LLM API testing.")
    parser.add_argument('--fields', type=str, help="Fields input for LLM API testing.")

    args = parser.parse_args()

    if args.action == 'ocr':
        suite = unittest.TestSuite()
        suite.addTest(APITestCases("test_send_to_ocr_api_success", file_path=args.file_path))
        # add other OCR related tests similarly
        unittest.TextTestRunner().run(suite)
    elif args.action == 'llm':
        suite = unittest.TestSuite()
        suite.addTest(APITestCases("test_send_to_llm_api_success", text=args.text, fields=args.fields))
        # add other LLM related tests similarly
        unittest.TextTestRunner().run(suite)

if __name__ == "__main__":
    main()
