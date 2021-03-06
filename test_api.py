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

import re
from flask import Flask, request, abort , make_response ,session
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

## 自定義 (google翻譯)
from google_translate import translate


app = Flask(__name__)

Channel_Access_Token = "15Nebz4rF/k9l0KsuYf9fIcMFIZrN4gvpHI7vGxyoWGa2rhF+NpPaA8KFehfLAKNfBKNP4jImjO8qKUzixj9NvirGAYfnoVP4OZKXMWQPnikZW0/7aMEumr7tRcxrz4cQbkUXcexJdidKcGHkjKk9QdB04t89/1O/w1cDnyilFU="
Secret = "f41a8267162f9ea5e0d877686b59bdac"

# Channel Access Token
line_bot_api = LineBotApi(Channel_Access_Token)
# Channel Secret
handler = WebhookHandler(Secret)

# pattern

translate_language_pattern = "^/語言"
translate_feature_pattern = "^%翻譯"


# global
mode_string = ""
lang = ""

@app.route("/ti/p/@cxw7652m?mac=<mac>")
def get_mac(mac):
    global mac_addr
    mac_addr = mac
    print(mac_addr)

@handler.add(FollowEvent)
def handle_follow(event):
    user_ID = event.source.user_id
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=f'{user_ID} \n {mac}'))



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
    global mode_string ,lang
    print("event =", event)
    
    data = event.postback.data 

    if data == "/進入翻譯模式" :
        #mode_string = "%翻譯"
        #lang = "en"
        session["mode_string"] = "%翻譯"
        session["lang"] = "en"
        text = "已進入翻譯模式(預設英文)，欲結束翻譯模式，請按離開翻譯模式"

    elif data == "/更換語言" :
        language_template =ButtonsTemplate(
            thumbnail_image_url="https://i.imgur.com/eTldj2E.png?1",
            title='翻譯語言更換', 
            text='Please select',
            image_size="cover",
            actions=[
    #           PostbackTemplateAction 點擊選項後，
    #           除了文字會顯示在聊天室中，
    #           還回傳data中的資料，可
    #           此類透過 Postback event 處理。
            PostbackTemplateAction(
                label='中文',
                data='/語言 zh-tw'
                ),
            PostbackTemplateAction(
                label='英文',
                data='/語言 en'
                ),
            PostbackTemplateAction(
                label='日文',
                data='/語言 ja'
                ),
            ]
        )
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text="Template Example",
                template=language_template
            )
        )
        text = None

    elif data == "/離開翻譯模式":
        #mode_string = ""
        #lang = ""
        session["mode_string"] = ""
        session["lang"] = ""
        text = "已離開翻譯模式"

    if re.match(translate_language_pattern , data):
        #lang = data.split(" ")[1]
        session["lang"] = data.split(" ")[1]
        text = "已轉換語系"

    print("mode_string 1 : " , mode_string)

    if text is None:
        return

    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(
            text=text,
        )
    )


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)

    mode_string = session.get("mode_string")
    lang = session.get("lang")

    print('global : ' , mode_string , lang)

    if mode_string != "" and mode_string != None:
        text = mode_string + event.message.text
    else :
        text = event.message.text

    print("text : " , text)
    user_ID = event.source.user_id

    user_profile = line_bot_api.get_profile(user_ID)

    user_name = user_profile.display_name
    user_picture = user_profile.picture_url
	
    ## 強制離開模式
    if (event.message.text == "%離開"):
        session["mode_string"] = ""
        session["lang"] = ""
        reply_text = "已離開"

    if (text == "翻譯") :
        #reply_text = "進入翻譯模式"
        #message = TextSendMessage(reply_text)
        #line_bot_api.reply_message(event.reply_token, message)
        button_template_message =ButtonsTemplate(
            thumbnail_image_url="https://i.imgur.com/eTldj2E.png?1",
            title='翻譯選項', 
            text='Please select',
            image_size="cover",
            actions=[
    #           PostbackTemplateAction 點擊選項後，
    #           除了文字會顯示在聊天室中，
    #           還回傳data中的資料，可
    #           此類透過 Postback event 處理。
                PostbackTemplateAction(
                    label='進入翻譯模式',
                    data='/進入翻譯模式'
                ),
                PostbackTemplateAction(
                    label='更換語言',
                    data='/更換語言'
                ),
                PostbackTemplateAction(
                    label='離開翻譯模式',
                    data='/離開翻譯模式'
                ),
            ]
        )
        reply_text = None
                            
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
        reply_text = f"{user_name},已離開功能模式"
#如果非以上的選項，就會學你說話

    if re.match(translate_feature_pattern,text):
        reply_text = translate(event.message.text , lang)
		
    if reply_text == None :
        return

    message = TextSendMessage(reply_text)
    print('reply message : ', message)
    line_bot_api.reply_message(event.reply_token, message)








import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)