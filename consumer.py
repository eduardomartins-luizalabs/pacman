import boto.sqs
import ConfigParser
import sys
import json
from boto.sqs.message import RawMessage
from datetime import datetime

def download_messages(queue_name):
    #Set up
    config = ConfigParser.RawConfigParser()
    config.read("pacman.properties")
    zone = config.get('SQS', 'aws_zone')
    access_key = config.get('SQS', 'aws_access_key')
    secret = config.get('SQS', 'aws_secret')
    path = config.get('IO', 'base_path')
    # Open connection
    conn = boto.sqs.connect_to_region(zone, aws_access_key_id=access_key, aws_secret_access_key=secret)
    # Getting messages
    q = conn.get_queue(queue_name)
    q.set_message_class(RawMessage)
    rs = q.get_messages(num_messages=10, attributes='All')
    all_messages = []
    while len(rs)>0:
        all_messages.extend(rs)
        rs = q.get_messages(num_messages=10, attributes='All')
    with open(path+queue_name+'.txt', 'w') as fl:
        for message in all_messages:
            write_message(message, fl)


def write_message(message, fl):
    body = message.get_body()
    attr = message.attributes
    date_formatted = datetime.fromtimestamp(long(str(attr['SentTimestamp'])[:-3])).strftime('%Y-%m-%d')
    hour_formatted = datetime.fromtimestamp(long(str(attr['SentTimestamp'])[:-3])).strftime('%H:%M:%S')
    j = json.loads(body)
    j[u'date'] = date_formatted
    j[u'hour'] = hour_formatted
    dumps = json.dumps(j, sort_keys=True)
    fl.write(dumps)
    fl.write('\n')


def main():
    for arg in sys.argv:
        if not arg == 'consumer.py': # Wanna fight about that?
            download_messages(arg)


if __name__ == "__main__":
    main()

