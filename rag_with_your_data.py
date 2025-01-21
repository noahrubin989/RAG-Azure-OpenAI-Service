# LIFESAVER: https://community.openai.com/t/error-with-openai-1-56-0-client-init-got-an-unexpected-keyword-argument-proxies/1040332/8
# pip install httpx==0.27.2

import os
import json
from typing import Tuple
from dotenv import load_dotenv
from openai import AzureOpenAI


def setup_oai_client() -> Tuple[AzureOpenAI, str]:
    """
    Sets up an Azure OpenAI client using environment variables.

    Returns:
        Tuple[AzureOpenAI, str]: A tuple containing the initialised Azure OpenAI client
        and the Azure OpenAI deployment name.
    """
    azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
    azure_oai_key = os.getenv("AZURE_OAI_KEY")
    azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
    
    # Initialise the Azure OpenAI client
    client = AzureOpenAI(
        base_url=f"{azure_oai_endpoint}/openai/deployments/{azure_oai_deployment}/extensions",
        api_key=azure_oai_key,
        api_version="2023-09-01-preview"
    )
    
    return client, azure_oai_deployment


def setup_azure_search() -> Tuple[str, str, str]:
    """
    Sets up the Azure Cognitive Search configuration using environment variables.

    Returns:
        Tuple[str, str, str]: A tuple containing the Azure Search endpoint, key,
        and index name.
    """
    azure_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    azure_search_key = os.getenv("AZURE_SEARCH_KEY")
    azure_search_index = os.getenv("AZURE_SEARCH_INDEX")
    return (
        azure_search_endpoint,
        azure_search_key,
        azure_search_index
    )


def main() -> None:
    """
    Main entry point of the script. Loads environment variables, sets up the
    Azure OpenAI client and Azure Cognitive Search configuration, prompts the
    user for input, and sends that request to the Azure OpenAI endpoint.
    """
    try:
        load_dotenv()

        # Flag to show citations
        show_citations = True

        client, azure_oai_deployment = setup_oai_client()
        azure_search_endpoint, azure_search_key, azure_search_index = setup_azure_search()

        # Get the prompt from user input
        text = input('\nEnter a question:\n')

        # Configure your data source
        extension_config = {
            "dataSources": [
                {
                    "type": "AzureCognitiveSearch",
                    "parameters": {
                        "endpoint": azure_search_endpoint,
                        "key": azure_search_key,
                        "indexName": azure_search_index,
                    }
                }
            ]
        }

        # Send request to Azure OpenAI model
        print("...Sending the following request to Azure OpenAI endpoint...")
        print(f"Request: {text}\n")

        response = client.chat.completions.create(
            model=azure_oai_deployment,
            temperature=0.5,
            max_tokens=1000,
            messages=[
                {"role": "system", "content": "You are a helpful travel agent"},
                {"role": "user", "content": text}
            ],
            extra_body=extension_config
        )

        # Print response
        print(f"Response: {response.choices[0].message.content}\n")

        if show_citations:
            # Print citations
            print("Citations:")
            citations = response.choices[0].message.context["messages"][0]["content"]
            citation_json = json.loads(citations)
            for c in citation_json["citations"]:
                print(f"Title: {c['title']}")
                # print(f"URL: {c['url']}")
                

    except Exception as ex:
        print('In the exception block')
        print(ex)


if __name__ == '__main__':
    main()
