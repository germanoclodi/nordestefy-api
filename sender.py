import pika, os

# Parse CLODUAMQP_URL (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL',"""amqp://""")
params = pika.URLParameters(url)
params.socket_timeout = 5
connection = pika.BlockingConnection(params) # Conectando ao CloudAMQP
channel = connection.channel() # Inicia um canal
channel.queue_declare(queue='positivo') # Declara a fila

# Publica a mensagem
channel.basic_publish(exchange='', routing_key='nordestefy', body='FITAS1|||FITAS2|||FITAS3')
print ("Mensagem enviada com sucesso!")
connection.close()