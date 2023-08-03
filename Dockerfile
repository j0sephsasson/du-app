# Pull the base image
FROM amazon/aws-lambda-python:3.7

# Copy reqs (from paddleocr repo)
COPY requirements.txt .

# Upgrade pip
RUN pip3 install --upgrade pip

# Install paddlepaddle
RUN python3 -m pip install paddlepaddle==2.0.0 -i https://mirror.baidu.com/pypi/simple

# Install protobuf
RUN pip3 install protobuf==3.20.0

# Install system dependencies
RUN yum -y update && yum install -y gcc gcc-c++ make libtool

# Install PaddleOCR dependencies
RUN pip3 install -r requirements.txt

# Install PaddleOCR
RUN pip3 install "paddleocr>=2.0.1"

## bug fix
RUN pip3 install --ignore-installed pymupdf==1.19.0

# Downgrade urllib3
RUN pip3 install urllib3==1.26.5

# Run PaddleOCR to download models
RUN python -c "from paddleocr import PaddleOCR; PaddleOCR()"

# Copy function code
COPY llm/ocr.py .

# Set the CMD to your handler
CMD ["ocr.lambda_handler"]