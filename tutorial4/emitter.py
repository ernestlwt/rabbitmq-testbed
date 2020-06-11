import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)

channel.queue_bind(exchange='direct_logs', queue=result.method.queue)

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World'

channel.basic_publish(
    exchange='direct_logs',
    routing_key=severity,
    body=message
)

print('[x] Sent %r:%r ' % (severity, message))
connection.close()