import boto.sqs
import ConfigParser
import sys

def download_messages(queue_name):
    config = ConfigParser.RawConfigParser()
    config.read("pacman.properties")
    zone = config.get('SQS', 'aws_zone')
    access_key = config.get('SQS', 'aws_access_key')
    secret = config.get('SQS', 'aws_secret')
    conn = boto.sqs.connect_to_region(zone, aws_access_key_id=access_key, aws_secret_access_key=secret)
    q = conn.get_queue(queue_name)
    rs = q.get_messages(10)
    all_messages = []
    while len(rs)>0:
        all_messages.extend(rs)
        rs = q.get_messages(10)
    path = config.get('IO', 'base_path')
    with open(path+queue_name+'.txt', 'w') as fl:
        for message in all_messages:
            fl.write(message.get_body() + '\n')

def main():
    for arg in sys.argv:
        if not arg == 'consumer.py': # Wanna fight about that?
            download_messages(arg)

if __name__ == "__main__":
    main()

