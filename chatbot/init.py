from librariesAndClass import *

# 3. Initialize the Azure-specific LangChain class
try:
    chat = AzureChatOpenAI(
        azure_deployment=deployment_name,
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        api_version=api_version,
        reasoning_effort=None,temperature=0.7,max_completion_tokens=500,top_p=0.9,
        max_retries=3,timeout=30
    )
except (OpenAIError, ValueError) as exc:
    raise RuntimeError(f"Failed to initialise AzureChatOpenAI: {exc}") from exc