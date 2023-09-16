import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

completion = openai.ChatCompletion.create(
  model = "gpt-3.5-turbo",
  temperature = 0.8,
  max_tokens = 2048,
  messages = [
    {"role": "system", "content": "You are a medical consultant. You will be provided information of a medicine. Your job is to summarize important information related to the medicine."},
    {"role": "user", "content": "Aspirin"}
  ]
)

print(completion.choices[0].message["content"])
