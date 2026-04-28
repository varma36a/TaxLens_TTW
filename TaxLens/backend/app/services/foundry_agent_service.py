from openai import AsyncAzureOpenAI
from app.config.settings import settings

client = None


def get_client():
    global client
    if not settings.is_azure_openai_configured:
        raise RuntimeError(
            "Azure OpenAI is not configured. Set AZURE_OPENAI_ENDPOINT, "
            "AZURE_OPENAI_API_KEY, and AZURE_OPENAI_DEPLOYMENT."
        )

    if client is None:
        client = AsyncAzureOpenAI(
            api_key=settings.azure_openai_api_key,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version="2024-02-01",
            timeout=30.0,
            max_retries=2,
        )

    return client

async def generate_tax_explanation(prompt: str):
    response = await get_client().chat.completions.create(
        model=settings.azure_openai_deployment,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an enterprise corporate tax analyst specializing in "
                    "tax explanations, comparisons, state obligations, "
                    "and strategic financial summaries."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    return response.choices[0].message.content
