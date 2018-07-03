import json
import sendmail
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
# Connect and block other rabbit
channel = connection.channel()
# Declare queue's name
channel.queue_declare(queue="importers")


# Declare importers
def importers(ch, method, properties, body):
    body = str(body)[2:-1:]
    body = json.loads(body)
    sendmail.enviar(body['body'], body['subject'], body['to'])
    print("The message was sent")
    # IF ACK IS ENABLE
    # ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(importers, queue="importers", no_ack=True)
# CON ACK FALSE
# channel.basic_consume(importers, queue="importers", no_ack=False)
print("Worker started")

channel.start_consuming()
