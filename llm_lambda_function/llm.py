import os, openai, shutil, json
from llama_index import Document, VectorStoreIndex, LLMPredictor, Prompt
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from typing import Any, List

load_dotenv()

os.environ['USE_TORCH'] = '1'
os.environ['OPENAI_API_KEY'] = str(os.getenv('OPENAI_API_KEY'))
openai.api_key = str(os.getenv('OPENAI_API_KEY'))

TEMPLATE = (
    "You are a helpful assistant that extracts specific information from unstructured data. That data is provided below\n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Given this information, please answer the question with precision: {query_str}\n"
)
QA_TEMPLATE = Prompt(TEMPLATE)

def extract_data(text:str, questions:List[str]) -> str:
    document = Document(text=text)

    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name='gpt-4'))
    index = VectorStoreIndex.from_documents([document], llm_predictor=llm_predictor)

    query_engine = index.as_query_engine(text_qa_template=QA_TEMPLATE)

    result_string = ""
    for q in questions:
        result_string += '---------------\n'
        # result_string += 'QUESTION:\n'
        # result_string += q + '\n'
        # result_string += 'ANSWER:\n'
        result_string += query_engine.query(q).response + '\n'

    return result_string

def lambda_handler(event, context):
    # Extract text and questions from the queryStringParameters.
    text = event["queryStringParameters"]['text']
    questions_string = event["queryStringParameters"]['questions']
    
    # Convert questions string to list.
    questions = questions_string.split(',')
    
    result = extract_data(text, questions)
    
    # Return the result.
    return {
        'statusCode': 200,
        'body': json.dumps({'result': result})
    }