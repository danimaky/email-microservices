import pika

import uuid





class FibonacciClient(object):



    def __init__(self):

        self.connection = pika.BlockingConnection(

            pika.ConnectionParameters('localhost')

        )



        self.channel = self.connection.channel()



        result = self.channel.queue_declare(exclusive=True)



        self.callback_queue = result.method.queue



        self.channel.basic_consume(self.on_response, queue=self.callback_queue, no_ack=False)



        self.response = None

        self.corr_id = None



    def on_response(self, ch, method, properties, body):

        if self.corr_id == properties.correlation_id:

            self.response = body



    def __call__(self, n):



        self.corr_id = uuid.uuid4().hex



        self.channel.basic_publish(

            exchange='',

            routing_key='fib',

            properties=pika.BasicProperties(

                reply_to=self.callback_queue,

                correlation_id=self.corr_id

            ),

            body=str(n)

        )



        while self.response is None:

            self.connection.process_data_events()



        return int(self.response)





client = FibonacciClient()

n = input("Number to do fib: ")

print("[*] Send {} to fibonacci".format(n))



response = client(n)



print("[*] Response = {}".format(response))