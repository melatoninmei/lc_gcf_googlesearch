# HTTP request to trigger chatGPT + google search 🚀

Example request:

```sh
curl --location --request GET 'http://localhost:8080' \
   --header 'Content-Type: application/json' \
   --data '{
      "question": "what'\''s the capital of cordova"
   }'
```

Will trigger this behaviour:

```
Recieved GET {'question': "what's the capital of cordova"}

> Entering new AgentExecutor chain...
 I need to find a reliable source to answer this question
Action: Search
Action Input: "capital of Cordova"
Observation: Rancho Cordova dentist, Capital Village Dental are dedicated to general, family, and cosmetic dentistry with services including dental exams, ... Dave Cordova. ACORE Capital. New York, New York, ... The California Capital Airshow will return September 23 – 24 at Mather Airport. ... This event takes place in the City of Rancho Cordova, which is part of the ...
Thought: I now know the final answer
Final Answer: {
    "result": "Córdoba, Spain is the capital of Cordova",
    "proof": "Córdoba or sometimes Cordova is a city in Andalusia, Spain, and the capital of the province of Córdoba.",
    "url": "https://www.google.com/search?q=capital+of+Cordova"
}
```

Responds with response:

```json
{
    "result": "Córdoba, Spain is the capital of Cordova",
    "proof": "Córdoba or sometimes Cordova is a city in Andalusia, Spain, and the capital of the province of Córdoba.",
    "url": "https://www.californiacapitalairshow.com/"
}
```

Based on a tutorial [here](https://medium.com/@zps270/a-comprehensive-guide-to-using-langchain-js-and-google-cloud-functions-for-ai-applications-426e0e83f0e6)

This is a fork of [LC_GCF](https://github.com/kulaone/LC_GCF)

# Getting Started 🧾

## Prerequisites

-   A Google Cloud account with an active project
-   Python (version 3.7 or higher) installed for the Python implementation
-   Google Cloud SDK installed and configured on your local machine

## Deployment 🏠

1. Clone this repository to your local machine:

2. Populate and source env file with credentials

See secrets section.

    Google CSE ID: [Google Programmable Search Engine](https://programmablesearchengine.google.com/controlpanel/all)

    Google API Key: [Google Cloud Console](https://console.cloud.google.com/apis/credentials)

    Get an OpenAI key here: [Open AI API Keys - you need an account with loaded credits](https://platform.openai.com/account/api-keys)

    `touch env.sh`:

    ```
    export GOOGLE_CSE_ID="XXXXXXXXXXXXXXXXX"
    export GOOGLE_API_KEY="XXXXXXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXXX"
    export OPENAI_API_KEY="XX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ```

3. Give executable permissions to deploy

    ```
    chmod +x ./deploy.sh
    ```

4. Deploy


```
firebase init
firebase deploy
```

## Secrets

```
firebase functions:secrets:set OPENAI_API_KEY
```

## Logs 🪵

```
source env.sh
gcloud functions logs read google-search-ai-http
```

## Run locally 👩🏻‍💻

1. Install dependencies

    ```
    pip install -r requirements.txt
    ```

2. Start up the server

    ```
    source env.sh
    functions-framework-python --target hello_http --debug
    ```

    More about running locally here: https://github.com/GoogleCloudPlatform/functions-framework-python

3. Hit with curl request outlined above

## License

This project is licensed under the [LICENSE NAME] License - see the [LICENSE](LICENSE) file for details.
