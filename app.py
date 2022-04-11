from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from pythainlp.tokenize import word_tokenize
from pythainlp.util import *
import numpy as np
from numpy import array
from gensim.models import Word2Vec
import difflib



app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Kwv12/0CJ6hXLI9wCRg07QxRnEyxXsKiBLcgFEBJ6cN36R/sLZX62S8lN23AUeVhtNSUOaNh+4t9PL2aJrb1yyEfu80KkVE1dZqhVKAMeBUXQyRIWtiu1BeWqbm0hKPd/1PvCRTx4KGoRzT/N06jyQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('cde1b2bee5efe6589af1a42c8e0e6dfb')

# callback Post Request
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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg_from_user = event.message.text
    message = TextSendMessage(msg_from_user)
    line_bot_api.reply_message(event.reply_token, message)

wv_model = Word2Vec.load('corpus.th.model')
word_list = wv_model.wv.index_to_key


def load_data(datafile):
    dataX = []
    dataY = []
    data = open(datafile, "r").read().lower()
    for i in data.split("\n\n"):
        a = i.split("\n")
        question = a[0]
        answer = a[1]
        dataX.append(question)
        dataY.append(answer)
    return dataX, dataY



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)