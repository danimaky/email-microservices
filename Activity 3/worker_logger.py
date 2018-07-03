import json
from filelogger import log
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

channel = connection.channel()
channel.exchange_declare(
    exchange='logs',
    exchange_type='direct'
)

results = channel.queue_declare(exclusive=True)

queue_name = results.method.queue

channel.queue_bind(exchange='logs', queue=queue_name, routing_key='info')
channel.queue_bind(exchange='logs', queue=queue_name, routing_key='warning')
channel.queue_bind(exchange='logs', queue=queue_name, routing_key='error')

print("[*] Starting worker logger with queue {}".format(queue_name))


def callback(ch, method, propierties, body):
    body = str(body)[2:-1:]
    body = json.loads(body)
    message = "[{}]: {} {} ".format(
        body['type'],
        body['code'],
        body['body'])
    log(message)
    print(message)


channel.basic_consume(callback, queue=queue_name)

channel.start_consuming()
