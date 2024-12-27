import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GAPI_KEY") #Enter your Generative AI API key here/your .env file

OWNER_ID = os.getenv("OWNER_ID") #Enter your Discord ID here/your .env file

CODE = os.getenv("CODE") #Enter your code here/your .env file

genai.configure(api_key=API_KEY)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Read multiple text files and concatenate their content
files = ['remmie.txt', 'rem_responses.txt']
combined_prompt = ""

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        combined_prompt += f.read() + "\n\n"

system_instruction = (
    combined_prompt
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
def gemini_response(user_input, user_id):
    
    # Check if the user is the owner
    if user_id == OWNER_ID:
        # Special response for the owner
        user_input = f"(This MSG IS From Belan, with User ID: {OWNER_ID}): {user_input}"  # Modify the input for the owner if needed
    else:
        user_input = f"(This MSG is NOT from Belan, they are User ID: {user_id}): {user_input}"
    # Send the message using the chat session
    response = chat_session.send_message(user_input)
    
    # Handle the response based on safety check
    if response.candidates[0].finish_reason == "SAFETY":
        return default_message  # If the response is flagged for safety, return a default message
    else:
        # Otherwise, concatenate the parts of the response to form the full response
        full_response = ''.join(part.text for part in response.candidates[0].content.parts)
        return full_response
    '''
    response = chat_session.send_message(user_input)
    if response.candidates[0].finish_reason == "SAFETY":
        return default_message
    else:
        full_response = ''.join(part.text for part in response.candidates[0].content.parts)
        return full_response
    '''