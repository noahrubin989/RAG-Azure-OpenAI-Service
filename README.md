# Retrieval Augmented Generation (RAG) with Azure OpenAI Service

## Overview
This repository details how GPT models and embedding models can be combined together to facillitate RAG workloads to augment prompts and draw meaningful information from your data sources. 

Azure OpenAI connects pre-trained models to your data sources to enabkle RAG ands utilises the search ability of Azure AI Search to add the relevant data chunks to the prompt. Once your data is in an AI Search index, Azure OpenAI on your data goes through the following steps:

1. Receive user prompt.
2. Determine relevant content and intent of the prompt.
3. Query the search index with that content and intent.
4. Insert search result chunk into the Azure OpenAI prompt, along with system message and user prompt.
5. Send entire prompt to Azure OpenAI.
6. Return response and data reference (if any) to the user.

By default, Azure OpenAI on your data encourages, but doesn't require, the model to respond only using your data. This setting can be unselected when connecting your data, which may result in the model choosing to use its pretrained knowledge over your data.

The data that had been added to the RAG solution is for a fictional travel company called "Margie’s Travel Agency" and has travel brochures for a variety of cities including:
* Dubai - `Dubai Brochure.pdf`
* Las Vegas - `Las Vegas.pdf` 
* London - `London.pdf` 
* New York - `New York.pdf` 
* San Francisco - `San Francisco.pdf`

_Note: The data used in `rag_with_your_data.py` resides in a personal blob storage container, but has been placed in a `data` folder for context on the data that was used._

## Configuration
To run this script you first need: 
* An Azure OpenAI resource.
* An Azure AI Search resource.
* An Azure Storage Account resource

Once the resources have been setup, it is possible to access the required values for the `.env` configuration file to include:

* The **endpoint** and a key from the Azure OpenAI resource you created (available on the **Keys and Endpoint** page for your Azure OpenAI resource in the Azure portal)
* The **deployment** name you specified for your gpt-35-turbo model deployment (available in the **Deployments** page in Azure AI Foundry portal).
* The **endpoint** for your search service (the **Url** value on the overview page for your search resource in the Azure portal).
* A **key** for your search resource (available in the **Keys** page for your search resource in the Azure portal - you can use either of the admin keys).
* The name of the search index.

The `.env` file would then take on the following form:

```
AZURE_OAI_ENDPOINT=your_azure_oai_endpoint
AZURE_OAI_KEY=your_azure_oai_key
AZURE_OAI_DEPLOYMENT=your_azure_oai_gpt_model_deployment_name
AZURE_SEARCH_ENDPOINT=your_azure_search_endpoint
AZURE_SEARCH_KEY=your_azure_search_key
AZURE_SEARCH_INDEX=your_named_search_index
```

## How to Run
Run the following `pip install` commands before running the code file:

```
pip install openai==1.13.3
pip install httpx==0.27.2
```

Then run `python3 rag_with_your_data.py`


## Resources
[Implementing RAG with the Azure OpenAI Service](https://learn.microsoft.com/en-gb/training/modules/use-own-data-azure-openai/1-introduction)


