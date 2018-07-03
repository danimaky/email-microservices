from celery import Celery

app = Celery("reto1", backend="amqp://guest:guest@localhost",  # amqp://guest:guest@localhost
             broker="amqp://localhost")

if __name__ == '__main__':
    app.start()