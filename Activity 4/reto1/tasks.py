import json
from filelogger import log
from client import app
from sendmail import enviar


@app.task
def send(type, code, body):
    if type == '2':
        message = "[{}]: {} {} ".format(
            type,
            code,
            body)
        enviar(message, 'Error Alert', 'danielsistem.ing96@gmail.com')
        print(message)
    return "Envio exitoso"


@app.task
def loger(type, code, body):
    body = str(body)[2:-1:]
    body = json.loads(body)
    message = "[{}]: {} {} ".format(
        type,
        code,
        body)
    log(message)
    return "Se ha registrado un registro"
loger.apply_async()