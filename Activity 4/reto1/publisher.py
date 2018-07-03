from kombu import messaging, Exchange

exchange = Exchange('reto1')
producer = messaging.Producer()
producer.publish(
    {'hello': 'world'},
    exchange=exchange # declares exchange, queue and binds.
)