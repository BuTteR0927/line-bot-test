from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, AudioSendMessage, VideoSendMessage

import tempfile, os
import datetime
import openai
import time

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
line_bot_api = LineBotApi('oOHxO8NXCxr6Ydaq8O7+69fVuE5cvG0EaBuVpr8wbKXok4/HdE89iTssfPsJCSKRsptDOL85aE2Bdy5dl9nOk/wxWKLYnHQbJA+Su6fRzV5ImuLRUTyPaqmRZWTihqtrZTl+DPVpbE7xlbnFJrxJlgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b3596d2b3029cebccf944a30d3b03592')

openai.api_key = os.getenv('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')

def GPT_response(text):
    # 接收回應
    response = openai.Completion.create(model="text-davinci-003", prompt=text, temperature=0.5, max_tokens=500)
    print(response)
    # 重組回應
    answer = response['choices'][0]['text'].replace('。','')
    return answer

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# baseurl = 'https://github.com/BuTteR0927/line-bot-test/tree/main/static/'  # 静态文件的网址

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    try:
        GPT_answer = GPT_response(mtext)
        print(GPT_answer)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('你所使用的OPENAI API key額度可能已經超過，請於後台Log內確認錯誤訊息'))
        
    if mtext == '@傳送聲音':
        try:
            message = AudioSendMessage(
                original_content_url=baseurl + 'rickroll.MP3',  # 声音文件位于static文件夹
                duration=20000  # 声音长度为20秒
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))
    elif mtext == '@傳送影片':
        try:
            message = VideoSendMessage(
                original_content_url=baseurl + 'rickroll.mp4',  # 视频文件位于static文件夹
                preview_image_url=baseurl + 'eggdog.jpeg'
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))
    elif mtext == '@傳送貼圖':
        try:
            message = StickerSendMessage(package_id='6362', sticker_id='11087922')
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))
    elif mtext == '@多項傳送':
        try:
            message = [
                StickerSendMessage(package_id='6632', sticker_id='11825377'),
                TextSendMessage(text="這是pizza圖片!"),
                ImageSendMessage(
                    original_content_url="https://i.imgur.com/0ooelxA.jpeg",
                    preview_image_url="https://i.imgur.com/0ooelxA.jpeg"
                )
            ]
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))
    elif mtext == '@傳送位置':
        try:
            message = LocationSendMessage(
                title='仙跡岩自然步道入口',
                address='116台北市文山區木柵',
                latitude=24.99388888888889,  # 緯度
                longitude=121.55825  # 經度
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))
    elif mtext == '@快速選單':
        try:
            message = TextSendMessage(
                text='請選擇最喜歡的程式語言',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="Python", text="Python")),
                        QuickReplyButton(action=MessageAction(label="Java", text="Java")),
                        QuickReplyButton(action=MessageAction(label="C#", text="C#")),
                        QuickReplyButton(action=MessageAction(label="Basic", text="Basic"))
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))
@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
