import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)

channel.queue_bind(exchange='logs', queue=result.method.queue)

def callback(ch, method, properties, body):
    print('[x] Received %r' % body)

channel.basic_qos(prefetch_count=1)
# default round robin is not good enough
# (e.g when you have 2 workers but every ODD-th job is more time consuming, ODD-th jobs will then always introduce delay)
# this line will then dispatch jobs only to available workers

channel.basic_consume(
    queue=result.method.queue,
    on_message_callback=callback,
    auto_ack=True
)


print('[*] Waiting for logs. To exit press CTRL+C')
channel.start_consuming()