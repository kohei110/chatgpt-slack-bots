import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Initialize a WebClient for making API requests
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

# Step 1: Ask the user to select a channel
@app.event("app_mention")
def message_hello(event, say):
    # Only respond to direct messages
    if event["channel_type"] == "im":
        # Get a list of available channels
        try:
            channels = client.conversations_list(types="public_channel,private_channel")["channels"]
            channel_options = [{"text": {"type": "plain_text", "text": c["name"]}, "value": c["id"]} for c in channels]
        except SlackApiError as e:
            print(f"Error: {e}")
            say("An error occurred while retrieving the list of channels. Please try again later.")
            return

        # Ask the user to select a channel
        say(
            text="Please select a channel:",
            blocks=[
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "static_select",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Select a channel"
                            },
                            "options": channel_options,
                            "action_id": "select_channel"
                        }
                    ]
                }
            ]
        )

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
