from dotenv import load_dotenv
import requests, os
from urllib.parse import quote

load_dotenv()

text = "<ocr extracted text here>"
questions = "Part number, Unit price, Amount"

api_url = str(os.getenv('LAMBDA_URL_LLM'))

# Properly encode parameters
encoded_text = quote(text)
encoded_questions = quote(questions)

api_url += f"?text={encoded_text}&questions={encoded_questions}"

response = requests.post(api_url)

# If success, print out the mapped questions and answers
if response.status_code == 200:
    # API returns JSON, parse the response
    data = response.json()

    print(data)

    for q, a in zip(questions.split(", "), data.get("result")):
        print(f"{q}: {a}")
else:
    print('message', 'Error occurred')