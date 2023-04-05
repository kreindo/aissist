import os
from dotenv import load_dotenv
load_dotenv
test = os.getenv("OPENAI_API_KEY")

print(test)