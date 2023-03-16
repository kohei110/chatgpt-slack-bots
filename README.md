# chatgpt-slack-bots

## Use-case

When you feel hard to catch up all of the active channels at Slack, Do you wanna get tldr or summary of the day? Yes, this is the one solution for this.
Open ai API backed Slack bot supports summarising eligible channels for you. 


## Summary
This Python script is a Slack bot that summarizes the chat history of a selected channel. It uses the Slack API to retrieve the conversation history and the OpenAI API to generate a summary of the conversation history. The bot listens to direct messages and responds with a list of available channels, and once a channel is selected, it generates a summary of the conversation history in the selected channel.

## Prerequisites

- Python 3
- Slack workspace
- Slack app token and bot token
- OpenAI API key
- slack-bolt and PyYAML packages

## Setup

Clone the repository and navigate to the project directory.
Install the required packages using pip install slack-bolt PyYAML.
Create a new bot user in your Slack workspace and obtain the app token and bot token.
Obtain an API key for OpenAI.
Create a config.yml file with the following information:

```
SLACK_APP_TOKEN: <your slack app token>
SLACK_BOT_TOKEN: <your slack bot token>
OPENAI_APIKEY: <your openai api key>
TXT_SELECT_CH: <message to prompt user to select a channel>
TXT_NOUPDATE: <message to display when there is no new message in the selected channel>
```


Run the script with python <filename.py>.

## How to use

- Direct message the bot in your Slack workspace.
- The bot will display a list of channels that the bot is a member of.
- Select a channel to generate a summary of the conversation history in the channel.
- The bot will respond with a summary of the conversation history, followed by any action items that were discussed in the conversation.
