import json
from sendmail import send
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

channel = connection.channel()

channel.exchange_declare(
    exchange='logs',
    exchange_type='fanout'
)

results = channel.queue_declare(exclusive=True)

queue_name = results.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)

print("[*] Starting worker error alert with queue {}".format(queue_name))


def callback(ch, method, propierties, body):
    body = str(body)[2:-1:]
    body = json.loads(body)
    if body['type'] == '2':
        message = "[{}]: {} {} ".format(
            body['type'],
            body['code'],
            body['body'])
        send(message, 'Error Alert', 'danielsistem.ing96@gmail.com')
        print(message)


channel.basic_consume(callback, queue=queue_name)

channel.start_consuming()
