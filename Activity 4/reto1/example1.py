from celery import Celery, chord
from sendmail import enviar

app = Celery("example1", backend="amqp://guest:guest@localhost",  # amqp://guest:guest@localhost
             broker="amqp://localhost")


@app.task(bind=True, queue="")
def add(self, x, y):
    return x + y


@app.task
def send(mensaje, asunto, destino):
    enviar(mensaje, asunto, destino)
    return "Envio exitoso"


class Multiply(app.Task):
    # Para obtener la información
    name = 'Multiply'
    queue = 'test '
    def run(self, x, y):
        return x * y


# multiply = app.tasks(Multiply.name)
app.register_task(Multiply())
