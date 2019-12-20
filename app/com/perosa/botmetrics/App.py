from flask import Flask, request, Response
import logging
import pyfiglet
import requests
import os

try:
    app = Flask(__name__)

    logging.basicConfig(level=logging.INFO)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
except Exception as e:
    logging.exception("Error at startup")


@app.route('/ping')
def ping():
    """
    Ping the endpoint
    :return:
    """
    logging.info('/ping')
    return "ping Ok"


@app.route('/send', methods=['POST'])
def send_to_botmetrics():
    """
    Endpoint
    :return:
    """
    try:
        logging.info('send/')

        # validate(request)

        api_key = request.headers['API_KEY']

        payload = request.get_json()
        headers = {'Content-Type': 'application/json'}

        if api_key is None:
            logging.warning("API_KEY is undefined")
            return "Not sent: API_KEY is undefined"
        else:

            text = get_text(payload)
            user_id = get_user_id(payload)
            json = get_json(text, user_id)

            logging.info("User text->" + text)

            p = {'token': api_key}
            r = requests.post("https://api.bot-metrics.com/v1/messages", params=p,
                              json=json, headers=headers)
            logging.info(r)
            return "ok"

    except Exception as e:
        logging.exception("Unexpected error")
        return Response(str(e), status=500)


def validate(request):
    token = os.getenv('BOTMETRICS_TOKEN', 'tokenUndefined')
    logging.info(token)

    header = request.headers['Authorization']
    logging.info(header)

    if header == None or (header != 'Bearer ' + token):
        raise Exception('Invalid token {} '.format(header))


def get_port():
    """
    Retrieves port
    :return:
    """
    return int(os.environ.get("PORT", 5000))


def get_json(text, user_id):
    data = {'text': text, 'message_type': 'incoming', 'user_id': user_id, 'platform': 'google'}

    return data


def get_text(payload):
    return payload['queryResult']['queryText']


def get_user_id(payload):
    return payload['session']


if __name__ == '__main__':
    ascii_banner = pyfiglet.figlet_format("BotMetrics Agent")
    print(ascii_banner)

    logging.info('Starting up')

    app.run(debug=True, port=get_port(), host='0.0.0.0')
