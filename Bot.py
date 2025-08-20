import telebot
import requests

# --- API KEYS ---
TELEGRAM_TOKEN = "8410022557:AAH-2vq82n3IlD9nOTAAmjahoWk-hBhB_SU"
GROQ_API_KEY = "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"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Groq se reply lene ka function
def chat_with_groq(message):
    url = "https://api.groq.com/openai/v1/chat/completions"   # ✅ correct endpoint
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",  # ✅ correct model name (Groq docs)
        "messages": [
            {"role": "system", "content": "You are a friendly AI friend who chats like a human."},
            {"role": "user", "content": message}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Error: {e}"

# --- Telegram handler ---
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_text = message.text
    bot.send_chat_action(message.chat.id, "typing")  # show typing...
    reply = chat_with_groq(user_text)
    bot.send_message(message.chat.id, reply)

print("🤖 Bot chal raha hai...")
bot.polling()
