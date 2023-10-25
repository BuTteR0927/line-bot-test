from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import openai
import time
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
# OPENAI API Key初始化設定
#openai.api_key = os.getenv('OPENAI_API_KEY')

'''def GPT_response(text):
    # 接收回應
    response = openai.Completion.create(model="text-davinci-003", prompt=text, temperature=0.5, max_tokens=500)
    print(response)
    # 重組回應
    answer = response['choices'][0]['text'].replace('。','')
    return answer '''

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

'''
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    try:
        GPT_answer = GPT_response(msg)
        print(GPT_answer)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        line_bot_api.reply_message(event.reply_token, TextSendMessage('发生错误，请检查日志以获取更多信息'))


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    try:
        GPT_answer = GPT_response(msg)
        print(GPT_answer)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('你所使用的OPENAI API key額度可能已經超過，請於後台Log內確認錯誤訊息'))


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
'''

baseurl = 'https://ef99-61-220-181-211.ngrok.io/static/'  # 静态文件的网址

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    if mtext == '@傳送聲音':
        try:
            message = AudioSendMessage(
                original_content_url="https://cdn.discordapp.com/attachments/1032361040253571123/1166650001066315856/rickroll.MP3?ex=654b427b&is=6538cd7b&hm=28f091fb5a8d490b8979e849c301b92fa97c12ba903d88ec1fce31eba6f65a48&",  # 声音文件位于static文件夹
                duration=20000  # 声音长度为20秒
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))
    elif mtext == '@傳送影片':
        try:
            message = VideoSendMessage(
                original_content_url="https://cdn.discordapp.com/attachments/1032361040253571123/1166650001548652554/rickroll.mp4?ex=654b427b&is=6538cd7b&hm=c836c099db854659c33d3e8dfc6168a38aeb882b912023fabaf9ce66e310339b&",  # 视频文件位于static文件夹
                preview_image_url="https://cdn.discordapp.com/attachments/1032361040253571123/1166650002202951781/eggdog.jpeg?ex=654b427b&is=6538cd7b&hm=934cb8646b473a4f8074314a42eb678934e5c669c79cdfd50083dfc241784f69&"
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

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
