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

@app.route("/callback/weather", methods=['GET'])
def weather(event):
    # get request body as text
    image = ImageSendMessage("https://www.mirrormedia.com.tw/assets/images/20181122160531-c07f2cf36f7e12424970da189de16567-mobile.jpg","https://www.mirrormedia.com.tw/assets/images/20181122160531-c07f2cf36f7e12424970da189de16567-mobile.jpg")
    line_bot_api.reply_message(event.reply_token, image)
    
	

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    text = event.message.text
    print(event.source.user_id)
    print(event.reply_token)
    user_ID = event.source.user_id
	
    user_profile = line_bot_api.get_profile(user_ID)

    user_name = user_profile.display_name
    user_picture = user_profile.picture_url
	
    if (text=="Hi"):
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

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)