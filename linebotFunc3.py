from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, AudioSendMessage, VideoSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi('oOHxO8NXCxr6Ydaq8O7+69fVuE5cvG0EaBuVpr8wbKXok4/HdE89iTssfPsJCSKRsptDOL85aE2Bdy5dl9nOk/wxWKLYnHQbJA+Su6fRzV5ImuLRUTyPaqmRZWTihqtrZTl+DPVpbE7xlbnFJrxJlgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b3596d2b3029cebccf944a30d3b03592')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

baseurl = 'https://ef99-61-220-181-211.ngrok.io/static/'  # 静态文件的网址

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
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

if __name__ == '__main__':
    app.run()
