from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import pika, os

app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from models import Location

@app.route('/api/run', methods=['POST'])
def run():                                                                                                                              
    # Parse CLODUAMQP_URL (fallback to localhost)
    url = os.environ.get('CLOUDAMQP_URL',"""amqp://""")
    params = pika.URLParameters(url)
    params.socket_timeout = 5
    connection = pika.BlockingConnection(params) # Conectando ao CloudAMQP
    channel = connection.channel() # Inicia um canal
    channel.queue_declare(queue='nordestefy') # Declara a fila
    
    # Define-se o método responsável por capturar as payloads enviadas à fila especificada
    # mais a frente, ao efetuar efetivamente o consumo da fila.
    def callback(ch, method, properties, body):
        data_str = str(body)
        data_str = data_str.replace("b", "")
        data_str = data_str.replace("'", "")
        print(" # RECEBI: " + data_str)
        data = data_str.split('|||')
        try:
            location=Location(
                longitude=data[0],
                latitude=data[1],
                datetime=data[2]
            )
            db.session.add(location)
            db.session.commit()
            return "Adicionado."
        except Exception as e:
            print(str(e))


    print(' # RECEPTOR ASSISTINDO A FILA nordestefy')
    
    # Define-se o serviço de consumo da fila especificada no campo queue, além de setar o serviço como
    # um watcher da fila, ao setar como True o auto_ack (auto-reconhecimento)
    channel.basic_consume(queue='nordestefy', auto_ack=True, on_message_callback=callback)
    
    # Efetivamente iniciar o consumo do serviço watcher
    channel.start_consuming()

    return "end"


@app.route('/api/get', methods=['GET'])
def get():
    try:
        locations=Location.query.all()
        return jsonify([e.serialize() for e in locations])
    except Exception as e:
        return(str(e))

