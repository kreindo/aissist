import os
import openai
from utils.prompter import *
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()


openai.organization = os.getenv('OPENAPI_ORG_KEY')
openai.api_key = os.getenv('OPENAI_API_KEY')

conversation = []
history = {"history": conversation}
mode = 0
total_char = 0


def defPrompt():
    result = input("Enter prompt: ")
    conversation.append({'role': 'user', 'content': result})
    openai_answer()


def openai_answer():
    global total_char, conversation

    for item in conversation:
        if isinstance(item, dict) and "content" in item:
            content = item["content"]
            total_char += len(content)

    while total_char > 4000:
        try:
            conversation.pop(2)
            total_char -= len(conversation[2]["content"])
        except:
            print("Error: Prompt too long!")

    with open("conversation.json", "w", encoding="utf-8") as f:
        # Write the message data to the file in JSON format
        json.dump(history, f, indent=4)

    prompt = getPrompt()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        max_tokens=128,
        temperature=1,
        top_p=0.9
    )
    message = response['choices'][0]['message']['content']
    print(message)
    conversation.append({'role': 'assistant', 'content': message})


if __name__ == "__main__":
    try:
        # You can change the mode to 1 if you want to record audio from your microphone
        # or change the mode to 2 if you want to capture livechat from youtube
        mode = input("Mode (1-Text, 2-Youtube Live): ")

        if mode == "1":
            while True:
                defPrompt()

        elif mode == "2":
            print("currently unimplemented")
            # live_id = input("Livestream ID: ")
            # # Threading is used to capture livechat and answer the chat at the same time
            # t = threading.Thread(target=preparation)
            # t.start()
            # get_livechat(live_id)
    except KeyboardInterrupt:
        print("Stopped")
