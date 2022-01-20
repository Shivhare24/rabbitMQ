import pika

url = 'amqps://utfvtbem:dAT1vSsYZDWhNpL9rsZzdGmYDc1mhzx9@lionfish.rmq.cloudamqp.com/utfvtbem'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()