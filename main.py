from flask import Flask, request, jsonify
import requests
import openai
import os

app = Flask(__name__)

# GPT API KEY
openai.api_key = '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'

# Telegram
BOT_TOKEN = '7944590947:AAGzJ9xsQVeiAnAcpSy8rOSx5SgCtB8Fk-Q'
CHAT_ID = '383196764'

# ============== GPT-відповідь ==============
@app.route('/gpt', methods=['POST'])
def gpt():
    data = request.json
    message = data.get('message', '')
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ти — веселий і турботливий консультант магазину одягу з поцілунками. Відповідай коротко, з емоцією, не забувай про уточнення кольору, розміру та доставки, якщо доречно."},
                {"role": "user", "content": message}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({"result": reply})
    except Exception as e:
        return jsonify({"result": f"⚠️ GPT error: {str(e)}"})

# ============== Сповіщення в Telegram ==============
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

# ============== Запуск ==============
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
