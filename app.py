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
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,ImageMessage, ButtonsTemplate, PostbackAction, MessageAction, TemplateSendMessage, URIAction
)

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))


@app.route('/')
def index():
    return 'OK'

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

    res = wolframalpha.Client(os.getenv("WOLFRAM_KEY")).query(f"{deeplres['translations'][0]['text']}")
    # print(res)

    buttontest = {
        "type": "template",
        "altText": "This is a buttons template",
        "template": {
            "type": "buttons",
            "thumbnailImageUrl": "https://www.nj.com/resizer/mg42jsVYwvbHKUUFQzpw6gyKmBg=/1280x0/smart/advancelocal-adapter-image-uploads.s3.amazonaws.com/image.nj.com/home/njo-media/width2048/img/somerset_impact/photo/sm0212petjpg-7a377c1c93f64d37.jpg",
            "imageAspectRatio": "rectangle",
            "imageSize": "cover",
            "imageBackgroundColor": "#FFFFFF",
            "title": "Menu",
            "text": "Please select",
            "defaultAction": {
            "type": "uri",
            "label": "View detail",
            "uri": "http://example.com/page/123"
            },
            "actions": [
            {
                "type": "postback",
                "label": "Buy",
                "data": "action=buy&itemid=123"
            },
            {
                "type": "postback",
                "label": "Add to cart",
                "data": "action=add&itemid=123"
            },
            {
                "type": "uri",
                "label": "View detail",
                "uri": "http://example.com/page/123"
            }
            ]
        }
        }
    buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://www.nj.com/resizer/mg42jsVYwvbHKUUFQzpw6gyKmBg=/1280x0/smart/advancelocal-adapter-image-uploads.s3.amazonaws.com/image.nj.com/home/njo-media/width2048/img/somerset_impact/photo/sm0212petjpg-7a377c1c93f64d37.jpg',
                title='Menu',
                text='Please select',
                actions=[
                    PostbackAction(
                        label='postback',
                        display_text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    MessageAction(
                        label='message',
                        text='message text'
                    ),
                    URIAction(
                        label='uri',
                        uri='http://example.com/'
                    )
                ]
            )
        )

    line_bot_api.reply_message(
            event.reply_token,
            # buttons_template_message
            TextSendMessage(text=f"{next(res.results).text}")
    )

if __name__ == "__main__":
    app.run()