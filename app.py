from flask import Flask, request, abort

import os
from dotenv import load_dotenv

import wolframalpha
import requests

load_dotenv()

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,ImageMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    q = event.message.text

    API_KEY = os.getenv("DEEPL_API_KEY")
    target_lang = 'EN'

    params_en = {
                'auth_key' : API_KEY,
                'text' : q,
                "target_lang": target_lang 
    }

    request = requests.post("https://api-free.deepl.com/v2/translate", data=params_en)
    deeplres = request.json()

    res = wolframalpha.Client("X2QW7H-AA3VJU6HJ4").query(f"{deeplres['translations'][0]['text']}")

    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"{next(res.results).text}")
    )

if __name__ == "__main__":
    app.run()