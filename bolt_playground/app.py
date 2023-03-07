import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime, timedelta
from slack_sdk.errors import SlackApiError

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Listens to incoming messages that contain "hello"
# @app.message("hello")
# def message_hello(message, say):
#     # say() sends a message to the channel where the event was triggered
#     say(
#         blocks=[
#             {
#                 "type": "section",
#                 "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
#                 "accessory": {
#                     "type": "button",
#                     "text": {"type": "plain_text", "text": "Click Me"},
#                     "action_id": "button_click"
#                 }
#             }
#         ],
#         text=f"Hey there <@{message['user']}>!"
#     )

@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")

@app.message("hiya")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hiya <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )


@app.message("hello")
def message_hello(message, say):
    try:
        # Calculate the timestamp for 24 hours ago
        oldest = datetime.timestamp(datetime.now() - timedelta(hours=24))
        # Call conversations.history API to retrieve messages from the last 24 hours
        history = app.client.conversations_history(channel=message["channel"], oldest=oldest)
        # print(history)
        # Filter out any messages posted by bots
        messages = [m for m in history["messages"] if "bot_id" not in m]
        # Extract the most recent message text from the conversation history
        message_text = {}
        username_list = []
        message_list = []
        for m in messages:
            if "user" in m and "text" in m:
                user_id = m["user"]
                # user_info = app.client.users_info(user=user_id)["user"]
                # if user_info["deleted"] or user_info["is_bot"]:
                #     continue
                # username_list.append(user_info["name"])
                username_list.append(user_id)                
                message_list.append(m["text"])
        for i in range(len(username_list)):
            message_text = {'username': username_list[i], 'text': message_list[i]}
        print(message_text)

        # print(message_text)
        # for m in messages:
        #     if "user" in m and "text" in m:
        #         message_text[m["user"]] = m["text"]
        # Send a message back to the channel with all non-bot messages posted in the last 24 hours
        # message_text_str = f"Hey there <@{message['user']}>! Here are all the non-bot messages posted in this channel in the last 24 hours:\n```{message_text}```"
        # say(
        #     blocks=[
        #         {
        #             "type": "section",
        #             "text": {"type": "mrkdwn", "text": message_text_str},
        #             "accessory": {
        #                 "type": "button",
        #                 "text": {"type": "plain_text", "text": "Click Me"},
        #                 "action_id": "button_click"
        #             }
        #         }
        #     ],
        #     text=message_text_str
        # )
    except SlackApiError as e:
        print(f"Error retrieving conversation history: {e}")

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
