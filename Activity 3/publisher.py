import json
from datetime import datetime
import pika
SEVERITIES = {
    "1": "info",
    "2": "warning",
    "3": "error"
}


def validar(opc):
    return opc == "1" or opc == "2" or opc == "3"


connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

channel = connection.channel()
# 'Direct' means that queue's just receive the message with sames Routing_Key
channel.exchange_declare(exchange='logs', exchange_type='direct')
while True:
    print("Types of message:")
    print("1 - Information message")
    print("2 - Warning message")
    print("3 - Error message")
    message_type = input("Input the message's type: ")
    if validar(message_type):
        message_type = SEVERITIES[message_type]
        break
message_code = str(datetime.now())
message_body = input("Input the message's body: ")
message_json = json.dumps({"type": message_type, "code": message_code, "body": message_body})

channel.basic_publish(exchange='logs',
                      routing_key=message_type,
                      body=message_json
                      )
print("[{}]: {} {} ".format(message_type, message_code, message_body))
connection.close()