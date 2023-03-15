# chatgpt-slack-bots

## Use-case

When you feel hard to catch up all of the active channels at Slack, Do you wanna get tldr or summary of the day? Yes, this is the one solution for this.
Open ai API backed Slack bot supports summarising eligible channels for you. 


## Set up

### Step1: Get API Keys
Create Slack app from here https://api.slack.com/apps and obtain App-Level Token and Bot User OAuth Token for this app.
Also get Open AI API key from https://platform.openai.com/

### Step2: Create config yaml for set up
Create yaml file for configrations.
This is the example for this script

TXT_SELECT_CH: 'This is message when you summon Bot
TXT_NOUPDATE: 'This is the text when there's no update in the last 24 hours'

OPENAI_APIKEY: 'xxxx'
SLACK_APP_TOKEN: "token/from/slack/api/platform/basic/infomation/tab"
SLACK_BOT_TOKEN: "token/from/slack/api/platform/OAuth&Permissions/tab"
