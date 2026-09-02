from app.enums import EmbeddingModels
import os
import time
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

class LLMServices():
    def __init__(self):
        self.client = OpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("OPENAI_SECRET_KEY"))

    def call_llm_model(self, messages: list):
        """
        Call the LLM model and return the response with retries on rate limit or transient errors.
        """
        max_retries = 3
        backoff_seconds = 2
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="nvidia/nemotron-3.5-lightning:free",
                    messages=messages
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.warning(f"LLM API attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt == max_retries - 1:
                    raise e
                time.sleep(backoff_seconds * (2 ** attempt))

    def embed_text(self, texts: list, model_name: EmbeddingModels=EmbeddingModels.LLAMA_NEMO_EMBED):
        """
        Generate text embeddings with exponential backoff retry.
        Raises exceptions on error to prevent returning error strings.
        """
        model, format_input = self.get_embed_model_with_input_format(texts, model_name)

        if not texts:
            return []

        try:
            response = self.client.embeddings.create(
                model=model,
                input=format_input
            )
            embeddings = [data.embedding for data in response.data]
            if not embeddings:
                raise ValueError(f"Empty embeddings response from model '{model}'")
            return embeddings
        except Exception as e:
            logger.warning(f"Embedding API attempt failed for model '{model}': {e}")
            raise e
    

    def get_embed_model_with_input_format(self, texts:list[str],model_name: EmbeddingModels):
        if model_name == EmbeddingModels.LLAMA_NEMO_EMBED:
            # Add input format for LLAMA_NEMO_EMBED
            """
            [
                {
                    "content": [
                    {"type": "text", "text": "Test2"},
                    {"type": "text", "text": "Test2"}
                    ]
                }
            ]
            """
            formatted_input = []
            formatted_input.append({"content": []})
            for text in texts:
                formatted_input[0]["content"].append({"type": "text", "text": text})

            return "nvidia/llama-nemotron-embed-vl-1b-v2:free", formatted_input
        else: # model_name == EmbeddingModels.LIQUID_LM:
            # TODO: Add input format for LIQUID_LM
            return "liquid/lfm-2.5-embedding-350m:free", texts


