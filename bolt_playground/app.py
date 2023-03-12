import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime, timedelta
from slack_sdk.errors import SlackApiError
import openai

import yaml
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)
    SLACK_APP_TOKEN = config['SLACK_APP_TOKEN']
    SLACK_BOT_TOKEN = config['SLACK_BOT_TOKEN']
    OPENAI_APIKEY = config['OPENAI_APIKEY']

openai.api_key = OPENAI_APIKEY

# Initializes your app with your bot token and socket mode handler
app = App(token=SLACK_BOT_TOKEN)

@app.event("message")
def message_hello(event, say, ack):
    channel_type = event["channel_type"]
    user_id = event["user"]

    # Set conversation scope to DM only
    if channel_type == "im":

        # Get channel list
        channels_list_response = app.client.conversations_list(types="public_channel,private_channel")
        channels = channels_list_response["channels"]
        bot_is_member_channels = [x for x in channels if x["is_member"] == True]

        # Create available channel list
        li_channel_options = [{"text": {"type": "plain_text", "text": c["name"]}, "value": c["id"]} for c in bot_is_member_channels]        
        li_channel_id = [x["value"] for x in li_channel_options]

        # Create approved channel list
        li_approved_channel_ids = [] 
        for channel_id in li_channel_id:
            members = app.client.conversations_members(channel=channel_id)["members"]
            if user_id in members:
                li_approved_channel_ids.append(channel_id)

        selected_channels = [channel for channel in li_channel_options if channel['value'] in li_approved_channel_ids]
        
        say(
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"サマリーを読みたいチャンネルを選んでください:"},
                    "accessory": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a channel",
                            "emoji": True
                        },
                        "options": selected_channels,
                        "action_id": "channel_select"
                    }
                }
            ],
            text=f"Hey there <@{event['user']}>!"
        )
    
    # Acknowledge the action
    ack()

@app.action("channel_select")
def select_channel(body, ack, say, client):
    try:
        # Get the selected channel ID
        selected_channel = body["actions"][0]["selected_option"]["value"]

        # Calculate the timestamp for 24 hours ago
        oldest = datetime.timestamp(datetime.now() - timedelta(hours=24))

        # Retrieve conversation history from the selected channel
        message_texts = []
        try:
            history = app.client.conversations_history(channel=selected_channel, oldest=oldest)
            messages = [m for m in history["messages"] if "bot_id" not in m]
            for m in messages:
                if "user" in m and "text" in m:
                    user_id = m["user"]
                    user_info = app.client.users_info(user=user_id)["user"]
                    if user_info["deleted"] or user_info["is_bot"]:
                        continue
                    username = user_info["name"]
                    message_text = m["text"]
                    ts = datetime.fromtimestamp(float(m["ts"])).strftime("%Y-%m-%d %H:%M:%S")
                    message_texts.append({'username': username, 'text': message_text, 'ts': ts})
        except SlackApiError as e:
            print(f"Error retrieving conversation history for channel {selected_channel}: {e}")
        
        if message_texts == []:
            summarised_txt = f'過去24時間に何もアップデートはありませんでした。'
        else:
            message_text_str = ""
            for item in message_texts:
                message_text_str += f"'{item['ts']}': {item['username']} said: '{item['text']}'\n"

            summariser = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f'''こちらが{selected_channel}チャンネルの過去24時間の会話のログです。\n\n{message_text_str}\n\n
                この会話のログを元に2つの文章を作ってください。\n\n
                1つ目の文章は会話の要約を300字程度に会話内容を要約してください。またこの1つ目の文章を要約と呼びます。\n\n
                その後2つ目の文章は会話からアクションアイテムが含まれる場合はそれを箇条書きで追記してください。またこの2つ目の文章をアクションアイテムと呼びます。\n\n''',
                temperature=0.7,
                max_tokens=300,
                stop=None
            )
            # print(summariser)
            summarised_txt = summariser["choices"][0]["text"]

        # Send a message with the conversation history
        say(
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"```{summarised_txt}```"}
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