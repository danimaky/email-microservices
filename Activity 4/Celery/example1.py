import json

from celery import Celery, chord
from kombu import Queue, Exchange

from sendmail import enviar
app = Celery("example1", backend="amqp://guest:guest@localhost",  # amqp://guest:guest@localhost
             broker="amqp://localhost")

exchange = Exchange('logs2', 'fanout')
app.conf.task_queues = (
    Queue('prueba', exchange=exchange, exclusive=True, durable=False),
    Queue('add1', exchange=exchange, durable=False),
    Queue('prueba2', exchange=exchange, exclusive=True, durable=False),
    Queue('main', exchange=exchange, exclusive=True, durable=False),
)


@app.task(bind=False)
def add(self, x, y):
    try:
        return x + y
    except Exception as exc:
        self.retry(exc=exc)


@app.task(bind=True, queue="prueba")
def prueba(self, body):
    body = str(body)[2:-1:]
    body = json.loads(body)
    if body['type'] == '2':
        message = "[{}]: {} {} ".format(
            body['type'],
            body['code'],
            body['body'])
        send(message, 'Error Alert', 'danielsistem.ing96@gmail.com')
        print(message)


@app.task(bind=True, queue="prueba2")
def prueba2(self, body):
    body = str(body)[2:-1:]
    body = json.loads(body)
    message = "[{}]: {} {} ".format(
        body['type'],
        body['code'],
        body['body'])
    print(message)


@app.task(bind=True)
def main(self, x, y):
    return chord(prueba(x, y), prueba2(x, y)).apply_async()


@app.task
def send(mensaje, asunto, destino):
    enviar(mensaje, asunto, destino)
    return "Envio exitoso"


class Multiply(app.Task):
    # Para obtener la información
    name = 'Multiply'
    queue = 'test '
    exchange = 'prueubin'

    def run(self, x, y):
        return x * y


# multiply = app.tasks(Multiply.name)
app.register_task(Multiply())
