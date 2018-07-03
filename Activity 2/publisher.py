import json
from datetime import datetime
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

channel = connection.channel()
# 'Fanout' means that every queue receives the message from the exchange
channel.exchange_declare(exchange='logs2', exchange_type='fanout', durable=True)

print("Types of message:")
print("1 - Information message")
print("2 - Error message")
message_type = input("Input the message's type")
message_code = str(datetime.now())
message_body = input("Input the message's body")
message_json = json.dumps({"type": message_type, "code": message_code, "body": message_body})

channel.basic_publish(exchange='logs2',
                      routing_key='',
                      body=message_json
                      )
print("[{}]: {} {} ".format(message_type, message_code, message_body))
connection.close()