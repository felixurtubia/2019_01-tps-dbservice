import psycopg2
import database_management
import json
import pika, os
from urllib.parse import urlparse


	#cur.execute("DROP TABLE deck, userdeck, card, userdeck_deck, test")
	#cur.execute("CREATE TABLE deck (id serial PRIMARY KEY, cardsMin integer, cardsMax integer, cardsCount integer, type varchar);")

	#cur.execute("CREATE TABLE userdeck (id serial PRIMARY KEY, idSideDeck integer, idMainDeck integer, idExtraDeck integer ,idUser integer, name varchar);")

	#cur.execute("CREATE TABLE card (id serial PRIMARY KEY, idWeb integer, idDeck integer);")

	#cur.execute("CREATE TABLE userdeck_deck (id serial PRIMARY KEY, id_deck integer, id_userdeck integer);")		

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
	




def conexion():
	conn = psycopg2.connect("host=database-tps.cghxllrdyqzh.us-east-1.rds.amazonaws.com dbname=database-tps user=postgres password=hola1234")
	cur = conn.cursor()
	return conn, cur

def publicar(data, queue):
	url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://riikuyvl:WtYUU4rdx0-UOTPE0yrObjMZt4WXuAxh@crane.rmq.cloudamqp.com/riikuyvl')
	url = urlparse(url_str)
	params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
	    credentials=pika.PlainCredentials(url.username, url.password))
	connection = pika.BlockingConnection(params)
	channel = connection.channel()
	channel.queue_declare(queue=queue)
	channel.basic_publish(
		exchange='', 
		routing_key=queue, 
		body=json.dumps(data)
		)
	return

def crear_mazo(ch, method, properties, body):
	"""
	params : {iduser integer, name string}
	"""
	conn, cur = conexion()
	parametros = json.loads(body)

	SQL = "INSERT INTO userdeck (iduser, name) VALUES (%s, %s);"
	data = (parametros['iduser'], parametros['name'])
	print(cur.execute(SQL, data))

	#print("Datos: {}".format(body))
	print("Se ha creado un mazo del usuario {} con nombre {}"
		.format(parametros["iduser"], parametros["name"]))
	
	conn.commit()
	cur.close()
	conn.close()
	return

def crear_mazo_secundario(ch, method, properties, body):
	"""
	params : {idUserDeck integer, cardsMin integer, cardsMax integer, 
				cardsCount integer, type string:{side, main, extra}}
	"""
	conn, cur = conexion()
	parametros = json.loads(body)

	SQL = "INSERT INTO deck (id_userdeck, cardsmin, cardsmax, cardscount, type) VALUES (%s, %s, %s, %s, %s);"
	data = (parametros["idUserDeck"],parametros["cardsMin"], parametros["cardsMax"], parametros["cardsCount"], parametros["type"] )
	cur.execute(SQL, data)
	conn.commit()
	cur.close()
	conn.close()
	print("Se ha creado un mazo secundario para el mazo {} de tipo {}"
		.format(parametros["idUserDeck"], parametros["type"]))
	return

def agregar_carta_mazo_secundario(ch, method, properties, body):
	"""
	params: {idweb, iddeck}
	"""
	conn, cur = conexion()
	parametros = json.loads(body)
	SQL = "INSERT INTO card (idweb, iddeck) VALUES (%s, %s);"
	data = (parametros["idweb"], parametros["iddeck"])
	cur.execute(SQL, data)

	conn.commit()
	cur.close()
	conn.close()
	print("Se ha agregado la carta {} al mazo secundario {}".format(parametros["idweb"], parametros["iddeck"]))
	return

def editar_mazo_usuario(ch, method, properties, body):
	conn, cur = conexion()
	conn.commit()
	cur.close()
	conn.close()
	print("Se ha editado el mazo del usuario")
	return

def remover_mazo(ch, method, properties, body):
	"""
	params: {id}
	"""
	conn, cur = conexion()
	parametros = json.loads(body)

	SQL =  "DELETE FROM userdeck WHERE id=%s;"
	data = (parametros["id"],)
	cur.execute(SQL, data)

	SQL2 = "DELETE FROM deck where id_userdeck=%s;"
	data2 = (parametros["id"])
	cur.execute(SQL2, data2)

	conn.commit()
	cur.close()
	conn.close()
	print("Se ha removido el mazo "+ parametros["id"] + "del usuario")
	return

def leer_mazo_usuario(ch, method, properties, body):
	"""
	params : {id}
	"""
	conn, cur = conexion()
	parametros = json.loads(body)
	
	SQL = "SELECT * FROM userdeck WHERE id=%s;"
	data = (parametros["id"],)
	cur.execute(SQL, data)
	encontrado = cur.fetchall()
	diccionario_mazo = dict()
	for mazo in encontrado:
		diccionario_mazo['id'] = mazo[0]
		diccionario_mazo['id usuario'] = mazo[1]
		diccionario_mazo['nombre de mazo'] = mazo[2]
		diccionario_mazo['mazos_secundarios'] = list()

	SQL2 = "SELECT * FROM deck WHERE id_userdeck=%s;"
	cur.execute(SQL2, data)
	encontrado2 = cur.fetchall()
	for mazo_secundario in encontrado2:
		diccionario_mazo['mazos_secundarios'].append(
			{
			'id': mazo_secundario[0], 
			'type':mazo_secundario[4],
			'cardsCount':mazo_secundario[3],
			'cardsmax':mazo_secundario[2], 
			}
			)


	conn.commit()
	cur.close()
	conn.close()
	print("Los datos del mazo son: {}".format(diccionario_mazo))

	ch.basic_publish(exchange='', 
		routing_key=properties.reply_to, 
		properties=pika.BasicProperties(
			correlation_id = properties.correlation_id),
		body=json.dumps(diccionario_mazo)
		)
	ch.basic_ack(delivery_tag=method.delivery_tag)
	print("Resultado enviado")
	return json.dumps(diccionario_mazo)

def remover_carta_mazo_secundario(ch, method, properties, body):
	"""
	params: {idmazo integer, idcarta integer}
	"""
	conn, cur = conexion()
	parametros = json.loads(body)

	SQL = "DELETE * FROM card WHERE id=%s AND iddeck=%s"
	data = (parametros["idcarta"], parametros["idmazo"])
	cur.execute(SQL, data)

	conn.commit()
	cur.close()
	conn.close()
	print("Se ha removido la carta {} del mazo secundario {}"
		.format(parametros["idcarta"], parametros["idmazo"]))
	return

def listar_mazo_usuario(ch, method, properties, body):
	"""
	params: {id_user integer}		
	"""
	conn, cur = conexion()
	parametros = json.loads(body)
	
	SQL = "SELECT * FROM userdeck WHERE iduser=%s;"
	data = (parametros["id_user"],)
	cur.execute(SQL, data)
	encontrado = cur.fetchall()
	conn.commit()
	cur.close()
	conn.close()
	print("Los mazos del usuario {} son: {}".format(parametros["id_user"],json.dumps(encontrado)))

	ch.basic_publish(exchange='', 
		routing_key=properties.reply_to, 
		properties=pika.BasicProperties(
			correlation_id = properties.correlation_id),
		body=json.dumps(encontrado)
		)
	ch.basic_ack(delivery_tag=method.delivery_tag)

	print("Resultado enviado")

	#publicar(data=encontrado, queue=q8_r)
	return json.dumps(encontrado)