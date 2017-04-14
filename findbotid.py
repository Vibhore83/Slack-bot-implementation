# Find Bot ID

import json
from slackclient import SlackClient

configfile = r"C:\Users\VJ\PycharmProjects\ChatBot\config.json"

def get_test_data(file_path):
    try:
        fp = open(file_path, 'rb')
        data = json.load(fp)
        return data
    except:
        print "Provide proper JSON file path"
        exit()

global token
# Fetch JSON config file data in variable
config_data = get_test_data(configfile)
token = config_data['SLACK_BOT_TOKEN']

BOT_NAME = 'aibot'

slack_client = SlackClient(token)

if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # Retrieve all users so we can find our bot
        users = api_call.get('members')
		# Parse users to find bot
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("Could not find bot user with the name " + BOT_NAME)