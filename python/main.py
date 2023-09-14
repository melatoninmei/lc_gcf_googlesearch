import functions_framework
from langchain.chat_models import ChatOpenAI

# To help construct our Chat Messages
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate

# To parse outputs and get structured data back
from langchain.output_parsers import StructuredOutputParser, ResponseSchema, PydanticOutputParser

# Helpers
import os
import json

from langchain.llms import OpenAI

# Agent imports
from langchain.agents import load_tools
from langchain.agents import initialize_agent

# Tool imports
from langchain.agents import Tool
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.utilities import TextRequestsWrapper

GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID', '86dc43f4082c74752')
GOOGLE_API_KEY = os.getenv(
    'GOOGLE_API_KEY', 'AIzaSyApvFgLwiXhzdQq-WkKnW8bAEAAz040GPA')
openai_api_key = os.getenv(
    'OPENAI_API_KEY', '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')

# chat = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo",
#                   openai_api_key=openai_api_key)

llm = OpenAI(temperature=0, openai_api_key=openai_api_key)


search = GoogleSearchAPIWrapper(
    google_api_key=GOOGLE_API_KEY, google_cse_id=GOOGLE_CSE_ID)
requests = TextRequestsWrapper()
toolkit = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to search google to answer questions about current events"
    ),
    Tool(
        name="Requests",
        func=requests.get,
        description="Useful for when you to make a request to a URL"
    ),
]

agent = initialize_agent(toolkit, llm, agent="zero-shot-react-description",
                         verbose=True, return_intermediate_steps=True)


@functions_framework.http
def hello_http(request):
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
        }
        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Origin': '*'
    }
    response = "todo"
    return (response, 200, headers)


def run(input):
    instruction = """ return the url, quote and justification from the link as a JSON blob:
    ```
    {
        "result": "{summary of observation}",
        "proof": "{text snippet that led to the observation}",
        "url": "{url of proof}
    }
    ```
    """

    response = agent({"input": input + instruction})
    result = response["output"]
    return result
