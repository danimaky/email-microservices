from celery import Celery
from kombu import Exchange, Queue

app = Celery("main", backend="amqp://guest:guest@localhost", broker="amqp://localhost")
exchange = Exchange('logs2', 'fanout')
app.conf.task_queues = (
    Queue('task1', exchange=exchange, exclusive=True, durable=True, routing_key=''),
    Queue('task2', exchange=exchange, exclusive=True, durable=True, routing_key=''),
    Queue('publisher', exchange=exchange, exclusive=True, durable=True, routing_key=''),
)
app.conf.task_routes = ([
    ('task1', {'queue': 'task1'}),
    ('task2', {'queue': 'task2'}),
    ('publisher', {'queue': 'publisher'}),
],)
app.conf.task_default_exchange = 'logs2'
app.conf.task_default_exchange_type = 'fanout'

@app.task
def task1():
    return "Working task1"


@app.task
def task2():
    return "Working task2"


@app.task
def publisher():
    print("publsiher")
    return "work"