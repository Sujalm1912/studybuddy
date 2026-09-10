import os 
from dotenv import load_dotenv 
from google import genai 
load_dotenv() 
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY")) 
response = client.models.generate_content( model="gemini-3.5-flash-lite", contents="Explain gravity to a 10-year-old in three lines.", ) 
print(response.text)