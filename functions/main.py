# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_functions import options
from firebase_functions.params import SecretParam

from firebase_admin import initialize_app

# Helpers
import os

from langchain.llms import OpenAI

# Agent imports
from langchain.agents import initialize_agent

# Tool imports
from langchain.agents import Tool
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.utilities import TextRequestsWrapper

GOOGLE_CSE_ID = SecretParam('GOOGLE_CSE_ID')
GOOGLE_API_KEY = SecretParam('GOOGLE_API_KEY')
OPENAI_API_KEY = SecretParam('OPENAI_API_KEY')


# @https_fn.on_request()
# def on_request_example(req: https_fn.Request) -> https_fn.Response:
#     return https_fn.Response("Hello world!")

initialize_app()


@https_fn.on_request(secrets=[GOOGLE_CSE_ID, GOOGLE_API_KEY, OPENAI_API_KEY], memory=options.MemoryOption.GB_1)
def hello_http(request):
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY.value)

    search = GoogleSearchAPIWrapper(
        google_api_key=GOOGLE_API_KEY.value, google_cse_id=GOOGLE_CSE_ID.value)
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

    print("Recieved", request.method, request.get_json())
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

    input = request.get_json().get("question")
    if not input or not isinstance(input, str) or len(input) == 0:
        return ("Invalid question", 400, headers)
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
    return (result, 200, headers)
