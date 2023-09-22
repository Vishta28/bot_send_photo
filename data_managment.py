import psycopg2

host = 'localhost'
user = 'test_user'
password = 'testuser'
db_name = 'testdb'

def create_table(user_id):
	conn = None
	try:
		conn = psycopg2.connect(
			host=host,
			database=db_name,
			user=user,
			password=password
		)
		conn.autocommit = True
		with conn.cursor() as cursor:  # курсор ходит по таблице и выполняет ('execute')
			cursor.execute('''CREATE TABLE IF NOT EXISTS photo_report(
			user_id BIGINT PRIMARY KEY,
			photo_check TEXT
			)''')
			cursor.execute(f'SELECT EXISTS(SELECT user_id FROM photo_report WHERE user_id = {user_id})')
			check_user_id = cursor.fetchone()[0]
			if check_user_id == 0:
				cursor.execute(f''' 
								INSERT INTO photo_report(user_id)
								VALUES ('{user_id}')
								''')
				cursor.execute('''UPDATE photo_report SET photo_check = 'done' WHERE user_id = %s''', (user_id,))
			else:
				cursor.execute('''UPDATE photo_report SET photo_check = 'done' WHERE user_id = %s''', (user_id,))
	except Exception as er:
		print(f'Error with postgres >>> {er}')
	finally:
		if conn is not None:
			conn.close()