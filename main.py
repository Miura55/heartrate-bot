from flask import Flask, request, abort, render_template
import os
import json
import base64
import urllib.parse
import requests
import numpy

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

app = Flask(__name__, static_folder='static')

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))


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
        """
        for event in parser.parse(body, signature):
            handle_message(event)
        """
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

    temperature = float(numpy.frombuffer(
        buffer=decoded, dtype='int16', count=1, offset=0)[0] / 100.0)


# Can be replaced with the function in SDK
def reply_with_request(event, msg):
    url = 'https://api.line.me/v2/bot/message/reply'
    payload = {"replyToken": event["replyToken"],
               "messages": [{"type": "text", "text": msg}]}
    headers = {'content-type': 'application/json',
               'Authorization': 'Bearer %s' % os.environ.get('CHANNEL_ACCESS_TOKEN')}
    requests.post(url, data=json.dumps(payload), headers=headers)
    return


if __name__ == "__main__":
    app.debug = True
    app.run()
