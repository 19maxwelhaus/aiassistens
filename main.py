from flask import Flask, request, jsonify
import requests
import openai
import time
import os

app = Flask(__name__)

# === Ключі (твій токен GPT і Telegram) ===
openai.api_key = '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'
BOT_TOKEN = '7944590947:AAGzJ9xsQVeiAnAcpSy8rOSx5SgCtB8Fk-Q'
CHAT_ID = '383196764'
ASSISTANT_ID = 'asst_HSbSLk1T0CkxBxNSKFaVNsGJ'

# === GPT-відповідь ===
@app.route('/gpt', methods=['POST'])
def gpt():
    data = request.json
    user_message = data.get('message', '')

    try:
        thread = openai.beta.threads.create()

        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )

        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        while True:
            run_status = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run_status.status == 'completed':
                break
            time.sleep(0.5)

        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        reply = messages.data[0].content[0].text.value

        return jsonify({"result": reply})

    except Exception as e:
        return jsonify({"result": f"⚠️ GPT error: {str(e)}"})

# === Сповіщення в Telegram ===
@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    username = data.get('username', 'невідомо')
    message = f"🔔 Оплата підтверджена!\nКлієнт: https://instagram.com/{username}\nПеревір вручну."

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }

    requests.post(telegram_url, json=payload)
    return 'ok', 200

# === Запуск сервера ===
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
