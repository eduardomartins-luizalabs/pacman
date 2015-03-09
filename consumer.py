import boto.sqs

def download_messages(queue_name):
    conn = boto.sqs.connect_to_region('ZONE', aws_access_key_id='<YOUR KEY>', aws_secret_access_key='<YOUR SECRET>')
    q = conn.get_queue(queue_name)
    all_messages=[]
    rs = q.get_messages(10)
    while len(rs)>0:
        all_messages.extend(rs)
        rs = q.get_messages(10)
    with open('FILE PATH', 'w') as fl:
        for message in all_messages:
            fl.write(message.get_body() + '\n')

def main():
    download_messages('YOUR QUEUE')

if __name__ == "__main__":
        main()
