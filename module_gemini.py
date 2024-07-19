from pyrogram import Client, filters
import google.generativeai as genai
import os
import json


with open("userbot.info", "r") as file:
    lines = file.readlines()
    prefix_userbot = lines[2].strip()

# Укажите ключ в файле gemini.info, получить его можно на https://aistudio.google.com/app/apikey
with open("gemini.info", "r") as file:
    lines = file.readlines()
    GEMINI_API_KEY = lines[0].strip()

cinfo = f"🧠`{prefix_userbot}gemini`"
ccomand = " Нейросеть Gemini."

genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

history_file = "chat_history.json"
if os.path.exists(history_file):
    with open(history_file, "r") as file:
        chat_history = json.load(file)
else:
    chat_history = []


def command_gemini(app):
    @app.on_message(filters.command("gemini", prefixes=prefix_userbot))
    def gemini_command(_, message):
        global chat_history
        input_text = message.text.split(" ", maxsplit=1)[1]

        if input_text.lower() == "clear":
            chat_history = []
            with open(history_file, "w") as file:
                json.dump(chat_history, file)
            message.reply_text("🧹 История чата очищена!")
            return

        chat_session = model.start_chat(
            history=chat_history
        )

        response = chat_session.send_message(input_text)
        chat_history.append({"user": input_text, "bot": response.text})

        with open(history_file, "w") as file:
            json.dump(chat_history, file)

        message.reply_text(response.text)

print("Модуль Gemini загружен.")
