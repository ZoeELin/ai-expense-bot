from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

from dotenv import load_dotenv

load_dotenv()
channel_secret = os.getenv("LINE_CHANNEL_SECRET")
channel_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

app = Flask(__name__)

# 建立 Messaging API 實例
line_bot_api = LineBotApi(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))

@app.route("/")
def index():
    return "LINE Expense Bot is running!"

@app.route("/webhook", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text
    reply = f"你說了：{user_msg}"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)