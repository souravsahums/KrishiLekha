import os
from dotenv import load_dotenv

load_dotenv(override=True)

from langchain_openai import AzureChatOpenAI

openai_api_base = os.getenv("AZURE_OPENAI_API_BASE")
openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai_model_name = os.getenv("AZURE_OPENAI_MODEL_NAME", "gpt-35-turbo")
openai_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo")


def load_llm():
    return AzureChatOpenAI(
        azure_endpoint=openai_api_base,
        api_key=openai_api_key,
        deployment_name=openai_deployment_name,
        openai_api_version=openai_api_version,
        temperature=0.4,
        max_tokens=1024,
    )
    
