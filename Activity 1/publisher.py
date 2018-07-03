import json

import pika
emaildestiny = input("Input email's destiny")
subject = input("Input email's subject")
msj = input("Input email's body")
sended = json.dumps({"to": emaildestiny, "subject": subject, "body": msj})
print(sended)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# Connect and block other rabbit
channel = connection.channel()
# Make a communication
channel.queue_declare(queue="importers")
# Make importers
channel.basic_publish(
    exchange="",
    routing_key="importers",
    body=sended
)
print("Done")
connection.close()

# JSON
# JSON.dump
# JSON.loads
