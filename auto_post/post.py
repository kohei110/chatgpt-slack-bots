import requests
import yaml

with open('config.yml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

TOKEN = config['TOKEN']
CHANNEL = 'slack-bot-creation'

url = "https://slack.com/api/chat.postMessage"
headers = {"Authorization": "Bearer "+TOKEN}
data  = {
   'channel': CHANNEL,
   'text': 'sukokoko'
}
r = requests.post(url, headers=headers, data=data)
print("return ", r.json())
