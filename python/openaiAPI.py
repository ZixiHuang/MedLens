import openai
import os
from dotenv import load_dotenv

def generate_response(patient_info: str, med_info: str):
    # Load environment variables from .env file
  load_dotenv()

  # Get API key from environment variable
  openai.api_key = os.getenv("OPENAI_API_KEY")
  completion = openai.ChatCompletion.create(
    model = "gpt-4",
    temperature = 0.8,
    max_tokens = 2048,
    messages = [
      {"role": "system", "content": "You are a medical consultant. You will be provided the information of a specific medicine in a keyworded manner and information of a patient. \
      Your response should include: use of the medicine, instructions to take the medicine, any warnings, if applicable. \
      Keep the response concise." },
      {"role": "user", "content": f'The patient information is as follows. {patient_info} \n \
       The medicine information is as follows. {med_info}' }
    ]
  )

  return completion.choices[0].message["content"]

# print(generate_response('no allergy', 'aspirin'))