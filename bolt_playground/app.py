import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime, timedelta
from slack_sdk.errors import SlackApiError

import yaml
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)
    SLACK_APP_TOKEN = config['SLACK_APP_TOKEN']
    SLACK_BOT_TOKEN = config['SLACK_BOT_TOKEN']

# Initializes your app with your bot token and socket mode handler
app = App(token=SLACK_BOT_TOKEN)

@app.event("message")
def message_hello(event, say):
    channel_type = event["channel_type"]
    if channel_type == "im":
        say(
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"Do you wanna TLDR?"},
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Shoot me!"},
                        "action_id": "button_click"
                    }
                }
            ],
            text=f"Hey there <@{event['user']}>!"
        )

@app.action("button_click")
def action_button_click(body, ack, say):
    try:
        # Calculate the timestamp for 24 hours ago
        oldest = datetime.timestamp(datetime.now() - timedelta(hours=24))

        # Call conversations.list API to get a list of public channels the bot is a member of
        channels_list_response = app.client.conversations_list(types="public_channel")
        channels = channels_list_response["channels"]

        # Retrieve conversation history from each public channel
        message_texts = []
        for channel in channels:
            try:
                history = app.client.conversations_history(channel=channel["id"], oldest=oldest)
                messages = [m for m in history["messages"] if "bot_id" not in m]
                for m in messages:
                    if "user" in m and "text" in m:
                        user_id = m["user"]
                        user_info = app.client.users_info(user=user_id)["user"]
                        if user_info["deleted"] or user_info["is_bot"]:
                            continue
                        username = user_info["name"]
                        message_text = m["text"]
                        message_texts.append({'username': username, 'text': message_text})
            except SlackApiError as e:
                print(f"Error retrieving conversation history for channel {channel['name']}: {e}")

        message_text_str = ""
        for item in message_texts:
            message_text_str += f"{item['username']} said: '{item['text']}'\n"

        # Send a message with the conversation history
        say(
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "Here are all the non-bot messages posted in public channels I'm a member of in the last 24 hours:"}
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"```{message_text_str}```"}
                }
            ]
        )
    except Exception as e:
        print(f"Error: {e}")

    # Acknowledge the action
    ack()

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()

