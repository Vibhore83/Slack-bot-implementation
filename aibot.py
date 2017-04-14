import json
import time
from slackclient import SlackClient
from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter

configfile = r"C:\Users\VJ\PycharmProjects\ChatBot\config.json"
def get_test_data(file_path):
    try:
        fp = open(file_path, 'rb')
        data = json.load(fp)
        return data
    except:
        print "Provide proper JSON file path"
        exit()

# Fetch JSON config file data in variable
config_data = get_test_data(configfile)
token = config_data['SLACK_BOT_TOKEN']
botid = config_data['BOT_ID']

c = CurrencyRates()
b = BtcConverter()

# Declare constants
AT_BOT = "<@" + botid + ">"
slack_client = SlackClient(token)

def handle_command(command, channel):
    response = "Data doesn't match"
    if command.startswith("help"):
        response = "Operations supported are: Rates, Convert & Bitcoin. \nCurrency supported is 'USD','EUR','INR','JPY','CAD','SGD'"
    elif command.startswith("rates"):
        array = command.split()
        if (len(array) == 5):
            print "Input validated"
            if (array[2] == "USD".lower() and array[4] == "EUR".lower()):
                response = c.get_rate('USD', 'EUR')
                print response
            elif (array[2] == "EUR".lower() and array[4] == "USD".lower()):
                response = c.get_rate('EUR', 'USD')
                print response
            elif (array[2] == "INR".lower() and array[4] == "EUR".lower()):
                response = c.get_rate('INR', 'EUR')
                print response
            elif (array[2] == "EUR".lower() and array[4] == "INR".lower()):
                response = c.get_rate('EUR', 'INR')
                print response
            elif (array[2] == "USD".lower() and array[4] == "INR".lower()):
                response = c.get_rate('USD', 'INR')
                print response
            elif (array[2] == "INR".lower() and array[4] == "USD".lower()):
                response = c.get_rate('INR', 'USD')
                print response
            elif (array[2] == "USD".lower() and array[4] == "SGD".lower()):
                response = c.get_rate('USD', 'SGD')
                print response
            elif (array[2] == "SGD".lower() and array[4] == "USD".lower()):
                response = c.get_rate('SGD', 'USD')
                print response
            elif (array[2] == "CAD".lower() and array[4] == "SGD".lower()):
                response = c.get_rate('CAD', 'SGD')
                print response
            elif (array[2] == "SGD".lower() and array[4] == "CAD".lower()):
                response = c.get_rate('SGD', 'CAD')
                print response
        else:
            print "Input specified is wrong"
            response = "Use string : Rates of <USD | INR | EUR> to <USD | INR | EUR>"
            print "Use string : Rates of <USD | INR | EUR> to <USD | INR | EUR>"

    elif command.startswith("bitcoin"):
        array = command.split()
        if (len(array) == 4):
            print "Input validated"
            if (array[3] == "USD".lower()):
                btcamount = b.get_latest_price('USD')
                response = btcamount
                print response
            elif (array[3] == "EUR".lower()):
                btcamount = b.get_latest_price('EUR')
                response = btcamount
                print response
            elif (array[3] == "INR".lower()):
                btcamount = b.get_latest_price('INR')
                response = btcamount
                print response
            elif (array[3] == "GBP".lower()):
                btcamount = b.get_latest_price('GBP')
                response = btcamount
                print response
            elif (array[3] == "JPY".lower()):
                btcamount = b.get_latest_price('JPY')
                response = btcamount
                print response
            elif (array[3] == "CAD".lower()):
                btcamount = b.get_latest_price('CAD')
                response = btcamount
                print response
            elif (array[3] == "SGD".lower()):
                btcamount = b.get_latest_price('SGD')
                response = btcamount
                print response
        else:
            print "Input specified is wrong"
            response = "Use string : Bitcoin price in <USD | INR | EUR>"
            print "Use string : Bitcoin price in <USD | INR | EUR>"

    elif command.startswith("convert"):
        array = command.split()
        if (len(array) == 5):
            amount = array[2]
            print "Input validated"
            if (array[1] == "USD".lower() and array[4] == "EUR".lower()):
                convertedamount = c.convert('USD', 'EUR', float(amount))
                response = convertedamount
                print response
            elif (array[1] == "EUR".lower() and array[4] == "USD".lower()):
                convertedamount = c.convert('EUR', 'USD', float(amount))
                response = convertedamount
                print response
            elif (array[1] == "INR".lower() and array[4] == "USD".lower()):
                convertedamount = c.convert('INR', 'USD', float(amount))
                response = convertedamount
                print response
            elif (array[1] == "USD".lower() and array[4] == "INR".lower()):
                convertedamount = c.convert('USD', 'INR', float(amount))
                response = convertedamount
                print response
            elif (array[1] == "INR".lower() and array[4] == "EUR".lower()):
                convertedamount = c.convert('INR', 'EUR', float(amount))
                response = convertedamount
                print response
            elif (array[1] == "EUR".lower() and array[4] == "INR".lower()):
                convertedamount = c.convert('EUR', 'INR', float(amount))
                response = convertedamount
                print response
            else:
                response = "Use string : Convert <USD | INR | EUR> <amount> to <USD | INR | EUR>"
        else:
            print "Input specified is wrong"
            print "Use string : Convert <USD | INR | EUR> <amount> to <USD | INR | EUR>"
            response = "Use string : Convert <USD | INR | EUR> <amount> to <USD | INR | EUR>"

    else:
        response = "Enter [<botname> help] for details"

    slack_client.api_call("chat.postMessage", channel=channel,text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID.")