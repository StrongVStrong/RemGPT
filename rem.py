import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GAPI_KEY") #Enter your Generative AI API key here/your .env file
genai.configure(api_key=API_KEY)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

with open('remmie.txt', 'r') as file:
    remmie = file.read()

system_instruction = (
    remmie
)

default_message = "I'm sorry, but I can't assist with that topic."

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction=system_instruction
)

chat_session = model.start_chat(
  history=[]
)
'''
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye come bac")
        break
    response = chat_session.send_message(user_input)
    if response.candidates[0].finish_reason == "SAFETY":
        print("Vegito:", default_message)
    else:
        full_response = ''.join(part.text for part in response.candidates[0].content.parts)
        print("Vegito:", full_response)

'''
def gemini_response(user_input):
    response = chat_session.send_message(user_input)
    if response.candidates[0].finish_reason == "SAFETY":
        return default_message
    else:
        full_response = ''.join(part.text for part in response.candidates[0].content.parts)
        return full_response