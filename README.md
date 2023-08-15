# SuperDocs: Modular Document Understanding (DU) Pipeline

SuperDocs is a revolutionary DU platform, but its real magic lies beneath the surface. With the integration of two state-of-the-art technologies — `paddleocr` and `llama_index` — it offers not just an application, but a suite of modular, containerized microservices. Each is ready for individual deployment, catering to bespoke needs.

**Live App URL:** [SuperDocs](https://www.superdocs.tech)

## 🌐 Architecture & Capabilities

### 1. **Flask Server (`app.py`)**
- An interactive frontend to test and demonstrate the capabilities of the backend microservices.
- Uses Redis to handle simultaneous requests, ensuring responsive and uninterrupted user experiences.

### 2. **OCR Lambda Function (paddleOCR)**
- A standalone service capable of turning images and scanned docs into machine-readable text.
- Comes in a Dockerized environment for easy, consistent deployment.
- Independent utility means you're not limited to using it within SuperDocs; deploy as your project needs.

### 3. **LLM Lambda Function (llama_index)**
- A separate vector storage and text analysis microservice.
- Also Dockerized, ensuring a streamlined deployment and scalability.
- Use it as an individual service or in tandem with the OCR function — your choice.

## The Modular Advantage 🧩
Each component in SuperDocs is not just a part of a whole but a whole in itself. Thanks to the Docker containers, you can plug-and-play these services as per your project's requirements. While SuperDocs is perfect for understanding and testing these capabilities, the true potential lies in the individual power and flexibility of each microservice.

## 🚀 Local Setup

### Prerequisites:
- Docker
- Python 3.x (for the Flask app)
- Redis Server (for the Flask app)

### Steps:

1. **Clone and Navigate**:
    ```bash
    git clone https://github.com/j0sephsasson/du-app.git
    cd du-app
    ```

2. **Environment Configuration**:
    - Ensure environment variables like `LAMBDA_OCR_API` and `LAMBDA_URL_LLM` are set.

3. **Docker Containers**:
    - OCR Lambda:
        ```bash
        cd ocr_lambda_function
        docker build -t ocr_lambda_container .
        ```
    - LLM Lambda:
        ```bash
        cd llm_lambda_function
        docker build -t llm_lambda_container .
        ```

4. **Run the Flask Application** (optional):
    ```bash
    python app.py
    ```

5. 🔍 **API Testing**:

    Here's how you can dive into the comprehensive testing:

    - **Direct API Interaction**:
    - Utilize the `send_to_ocr_api(file_path)` and `send_to_llm_api(text, fields)` functions to directly interact with the APIs. Make sure the environment variables (`LAMBDA_OCR_API` and `LAMBDA_URL_LLM`) are correctly set for this purpose.

    - **Extensive Test Scenarios**:
    Our test suite (`api_testing/tests.py`) covers a broad spectrum of scenarios, from success cases, HTTP errors, timeouts, connection issues, to even unanticipated non-JSON responses.
    
    - **Mock Testing**: 
    Leveraging Python's `unittest.mock` library, we've constructed tests that are swift and independent of the external services' uptime.

    - **Distinct OCR & LLM Tests**:
    Both the `paddleocr` and `llm_lambda_function` APIs have their specific sets of tests ensuring the nuances of each service are captured accurately.

    - **CLI for Dynamic Testing**: 
    With `api_testing/cli.py`, engage in an interactive testing experience:
    1. **For OCR API**:
        ```bash
        python cli.py --action ocr --file_path [path_to_your_file]
        ```
    2. **For LLM API**:
        ```bash
        python cli.py --action llm --text "Your text here" --fields "Your fields here"
        ```

    Dive in and experience the reliability firsthand!

## 🔗 Access & Deployment

The modular architecture gives you multiple ways to utilize SuperDocs:

1. **Hosted APIs**: For those wanting a hassle-free experience, get in touch for direct access to the hosted APIs.
2. **Your Own APIs**: Feel empowered to deploy your own instances of the microservices. With Docker files and comprehensive documentation, creating your bespoke APIs is just a few commands away.

## 📢 In Conclusion

SuperDocs breaks the mold of monolithic applications. By providing individually containerized, scalable, and deployable microservices, it redefines flexibility in the DU domain. Whether you're a developer aiming for seamless integration or an enterprise seeking tailored solutions, SuperDocs is more than an app; it's a toolkit.

For feedback, collaborations, or support, please connect with me or drop an issue in the repository.