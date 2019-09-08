import psycopg2


def create_database():
	con = psycopg2.connect("host=database-tps.cghxllrdyqzh.us-east-1.rds.amazonaws.com dbname=database-tps user=postgres password=hola1234")
	cur = con.cursor()

	#cur.execute("DROP TABLE deck, userdeck, card, userdeck_deck, test")
	#cur.execute("CREATE TABLE deck (id serial PRIMARY KEY, cardsMin integer, cardsMax integer, cardsCount integer, type varchar);")

	#cur.execute("CREATE TABLE userdeck (id serial PRIMARY KEY, idSideDeck integer, idMainDeck integer, idExtraDeck integer ,idUser integer, name varchar);")

	#cur.execute("CREATE TABLE card (id serial PRIMARY KEY, idWeb integer, idDeck integer);")

	#cur.execute("CREATE TABLE userdeck_deck (id serial PRIMARY KEY, id_deck integer, id_userdeck integer);")		
	cur.execute("INSERT INTO deck (cardsMin, cardsMax, cardsCount, type) VALUES (%s, %s, %s, %s)", (0, 60, 0, "main_deck"))

	cur.execute("SELECT * FROM deck;")
	print(cur.fetchall())

	con.commit()
	cur.close()
	con.close()
	return 