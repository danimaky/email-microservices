import pika



connect = pika.BlockingConnection(

    pika.ConnectionParameters('localhost')

)



channel = connect.channel()



channel.queue_declare(queue='fib')





def fib(n):

    if n == 0:

        return 0

    if n == 1:

        return 1

    else:

        return fib(n - 1) + fib(n - 2)





def callaback(ch, method, properties, body):

    n = int(body)

    print("[*] Fib({})".format(n))



    response = fib(n)



    ch.basic_publish(exchange='',

                     routing_key=properties.reply_to,

                     properties=pika.BasicProperties(

                         correlation_id=properties.correlation_id

                     ),

                     body=str(response)

    )



    ch.basic_ack(delivery_tag=method.delivery_tag)





channel.basic_consume(callaback, queue='fib')



print("[*] Starting consuming")



channel.start_consuming()