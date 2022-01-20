import pika
import uuid
import time

class FibonacciRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.URLParameters(url='amqps://utfvtbem:dAT1vSsYZDWhNpL9rsZzdGmYDc1mhzx9@lionfish.rmq.cloudamqp.com/utfvtbem'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='rpc_queue_return', exclusive=True, durable=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        
        if int(self.response) % 2 == 0:
            return int(self.response)
        else:
            time.sleep(50)
            return int(self.response)


fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(10)
print(" [.] Got %r" % response)