from core.config import settings
from openai import OpenAI
import os

class LLMServices():
    def __init__(self):
        self.client = OpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("OPENAI_SECRET_KEY"))


    def call_llm_model(self,messages:list):
        """
        Call the LLM model and return the response
        """
        try:
            response = self.client.chat.completions.create(
                model="nvidia/nemotron-3.5-lightning:free",
                messages=messages
                )
            print("Response from LLM: ",response)
            return response.choices[0].message.content
        except Exception as e:
            return str(e)
    
    def embed_text(self,texts:list, model:str = settings.EMBEDDING_MODEL):
        try:
            response = self.client.embeddings.create(
                model=model,
                input=texts
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            return str(e)

