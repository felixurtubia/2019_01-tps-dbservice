import pika
import json 
import psycopg2

import methods


import pika, os
from urllib.parse import urlparse

# Parse CLODUAMQP_URL (fallback to localhost)
url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://riikuyvl:WtYUU4rdx0-UOTPE0yrObjMZt4WXuAxh@crane.rmq.cloudamqp.com/riikuyvl')
url = urlparse(url_str)
params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
    credentials=pika.PlainCredentials(url.username, url.password))

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
"""
connection = pika.BlockingConnection(
	pika.ConnectionParameters(
        host='amqp://riikuyvl:WtYUU4rdx0-UOTPE0yrObjMZt4WXuAxh@crane.rmq.cloudamqp.com/riikuyvl'
        ))
#connection = pika.BlockingConnection(
#	pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
"""

#Se definen las colas a utilizar
q1='crear_mazo'
q1_r='crear_mazo_respuesta'
q2='crear_mazo_secundario'
q2_r= 'crear_mazo_secundario_respuesta'
q3='agregar_carta_mazo_secundario'
q3_r='agregar_carta_mazo_secundario_respuesta'
q4='editar_mazo_usuario'
q4_r='editar_mazo_usuario_respuesta'
q5='remover_mazo'
q5_r='remover_mazo_respuesta'
q6='leer_mazo_usuario'
q6_r='leer_mazo_usuario_respuesta'
q7='remover_carta_mazo_secundario'
q7_r='remover_carta_mazo_secundario_respuesta'
q8 = 'listar_mazo_usuario'
q8_r = 'listar_mazo_usuario_respuesta'

q11 = 'ver_informacion_basica'
q11_r = 'ver_informacion_basica_respuesta'
q12 = 'ver_informacion_detallada'
q12_r = 'ver_informacion_detallada_respuesta'
q13 = 'busqueda_parcial'
q13_r = 'busqueda_parcial_respuesta'
q14 = 'busqueda_especifica' 
q14_r = 'busqueda_especifica_respuesta'

#Se crean las colas si no existen, caso contrario se comprueba su funcionamiento
channel.queue_declare(queue=q1)
channel.queue_declare(queue=q1_r)
channel.queue_declare(queue=q2)
channel.queue_declare(queue=q2_r)
channel.queue_declare(queue=q3)
channel.queue_declare(queue=q3_r)
channel.queue_declare(queue=q4)
channel.queue_declare(queue=q4_r)
channel.queue_declare(queue=q5)
channel.queue_declare(queue=q5_r)
channel.queue_declare(queue=q6)
channel.queue_declare(queue=q6_r)
channel.queue_declare(queue=q7)
channel.queue_declare(queue=q7_r)
channel.queue_declare(queue=q8)
channel.queue_declare(queue=q8_r)

channel.queue_declare(queue=q11)
channel.queue_declare(queue=q11_r)
channel.queue_declare(queue=q12)
channel.queue_declare(queue=q12_r)
channel.queue_declare(queue=q13)
channel.queue_declare(queue=q13_r)
channel.queue_declare(queue=q14)
channel.queue_declare(queue=q14_r)

channel.basic_consume(queue=q1,on_message_callback=methods.crear_mazo,auto_ack=True)
channel.basic_consume(queue=q2,on_message_callback=methods.crear_mazo_secundario,auto_ack=True)
channel.basic_consume(queue=q3,on_message_callback=methods.agregar_carta_mazo_secundario,auto_ack=True)
channel.basic_consume(queue=q4,on_message_callback=methods.editar_mazo_usuario,auto_ack=True)
channel.basic_consume(queue=q5,on_message_callback=methods.remover_mazo,auto_ack=True)
channel.basic_consume(queue=q6,on_message_callback=methods.leer_mazo_usuario)
channel.basic_consume(queue=q7,on_message_callback=methods.remover_carta_mazo_secundario,auto_ack=True)
channel.basic_consume(queue=q8,on_message_callback=methods.listar_mazo_usuario)
channel.basic_consume(queue=q11,on_message_callback=methods.get_data)
channel.basic_consume(queue=q12,on_message_callback=methods.get_data)
channel.basic_consume(queue=q13,on_message_callback=methods.get_data)
channel.basic_consume(queue=q14,on_message_callback=methods.get_data)


"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'database-tps',
        'USER': 'postgres',
        #'USER': 'master',
          'PASSWORD': 'hola1234',
        #'PASSWORD': 'cde56fgh76',
        'HOST': 'database-tps.cghxllrdyqzh.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
    }
"""









print('[x] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()