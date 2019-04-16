#from _future_ import print_function
#from apiclient.discovery import build
#from httplib2 import Http
#from oauth2client import file, client, tools

#import time
#import re
#import datetime
#import random
#import codecs
#import sys
#import json

from flask import Flask, request, abort
from urllib.request import urlopen
#from oauth2client.service_account import ServiceAccountCredentials

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,LineBotApiError
)

################################

from linebot.models import *

app = Flask(__name__)

Channel_Access_Token = "15Nebz4rF/k9l0KsuYf9fIcMFIZrN4gvpHI7vGxyoWGa2rhF+NpPaA8KFehfLAKNfBKNP4jImjO8qKUzixj9NvirGAYfnoVP4OZKXMWQPnikZW0/7aMEumr7tRcxrz4cQbkUXcexJdidKcGHkjKk9QdB04t89/1O/w1cDnyilFU="
Secret = "f41a8267162f9ea5e0d877686b59bdac"

# Channel Access Token
line_bot_api = LineBotApi(Channel_Access_Token)
# Channel Secret
handler = WebhookHandler(Secret)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    print("body : " , body)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(PostbackEvent)
def handle_post_message(event):
# can not get event text
    print("event =", event)
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(
            text=str(str(event.postback.data)),
        )
    )


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    text = event.message.text
    user_ID = event.source.user_id
	
    user_profile = line_bot_api.get_profile(user_ID)

    user_name = user_profile.display_name
    user_picture = user_profile.picture_url
	
    if (text == "翻譯") :
		button_template_message =ButtonsTemplate(
            thumbnail_image_url="https://i.imgur.com/eTldj2E.png?1",
            title='Menu', 
            text='Please select',
            image_size="cover",
            actions=[
    #           PostbackTemplateAction 點擊選項後，
    #           除了文字會顯示在聊天室中，
    #           還回傳data中的資料，可
    #           此類透過 Postback event 處理。
            PostbackTemplateAction(
                label='查詢個人檔案顯示文字-Postback', 
                text='查詢個人檔案',
                data='action=buy&itemid=1'
                ),
            PostbackTemplateAction(
                label='不顯示文字-Postback', 
                text = None,
                data='action=buy&itemid=1'
                ),
            MessageTemplateAction(
                label='查詢個人檔案-Message', text='查詢個人檔案'
                ),
            ]
        )
                            
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text="Template Example",
                template=button_template_message
            )
        )
    elif (text=="Hi"):
        reply_text = f"{user_name} , Hello"
        #Your user ID

    elif(text=="你好"):
        reply_text = "哈囉"
    elif(text=="機器人"):
        reply_text = "叫我嗎"
    else:
        reply_text = f"{user_name},{user_ID},{user_picture} , Hello"
#如果非以上的選項，就會學你說話

    message = TextSendMessage(reply_text)
    print('reply message : ', message)
    line_bot_api.reply_message(event.reply_token, message)

def translate()


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)