from flask import Flask, request, abort, render_template
import os
import json
import base64
import urllib.parse
import requests
import numpy

from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

CHANNEL_ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')


line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(CHANNEL_SECRET)


app = Flask(__name__, static_folder='static')

@app.route('/')
def do_get():
    return render_template('index.html')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        # Python SDK doesn't support LINE Things event
        # => Unknown event type. type=things
        for event in parser.parse(body, signature):
            handle_message(event)

        # Parse JSON without SDK for LINE Things event
        events = json.loads(body)
        for event in events["events"]:
            if "things" in event:
                handle_things_event(event)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

def handle_things_event(event):
    if event["things"]["type"] != "scenarioResult":
        return
    if event["things"]["result"]["resultCode"] != "success":
        app.logger.warn("Error result: %s", event)
        return

    # Read value end decode
    decoded = base64.b64decode(
        event["things"]["result"]["bleNotificationPayload"])
    button_state = float(numpy.frombuffer(
        buffer=decoded, dtype='int16', count=1, offset=0)[0])
    app.logger.info("Got data: " + str(button_state))
    if button_state > 0:
        line_bot_api.reply_message(event["replyToken"],
            TextSendMessage(text="Heart_rate: " + str(button_state)))

def handle_message(event):
    if event.type == "message" and event.message.type == "text":
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.debug = True
    app.run()
