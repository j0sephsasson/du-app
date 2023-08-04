FROM amazon/aws-lambda-python:3.9

COPY llm.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["llm.lambda_handler"]