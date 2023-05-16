from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import re
import os
import time
import pickle
import json
from bardapi import Bard

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
os.environ['_BARD_API_KEY']=os.getenv("BARD_API_KEY")

app = App(token=SLACK_BOT_TOKEN)

@app.message("hello slackbot!")
def message_hello(message, say):
    say("hi")

@app.event("app_mention")
def message_mention(body, say):
    event = body["event"]
    message = body["event"]["text"]
    user = body["event"]["user"]
    channel = body["event"]["channel"]
    identifier = user + channel
    user_input = re.sub('^\S+\s', '', message)

    response = Bard().get_answer(user_input)['content']

    if event.get("thread_ts") is None:
        say(response)
    else:
        say(text=response, thread_ts=body["event"]["thread_ts"])

if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()

