import os
import sys
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from openai import OpenAIError

print("Test checking")


env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", ".env")
if not os.path.isfile(env_path):
    raise FileNotFoundError(f"Configuration file not found: {os.path.normpath(env_path)}")
load_dotenv(env_path)
#Extract values from your .env configuration
api_key = os.getenv("AZURE_API_KEY")
azure_endpoint = os.getenv("AZURE_ENDPOINT")
deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")
api_version = os.getenv("AZURE_API_VERSION")

_required = {
    "AZURE_API_KEY": api_key,
    "AZURE_ENDPOINT": azure_endpoint,
    "AZURE_DEPLOYMENT_NAME": deployment_name,
    "AZURE_API_VERSION": api_version,
}
_missing = [name for name, value in _required.items() if not value]
if _missing:
    raise EnvironmentError(f"Missing values in {os.path.normpath(env_path)}: {', '.join(_missing)}")


