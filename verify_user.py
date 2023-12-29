import sqlite3
import json

class VerifyUserData(object):
	def __init__(self):
		self._DB = "usuarios.db"
	def verify_already_exists(self,user_id):
		conn = sqlite3.connect('usuarios.db')
		cursor = conn.cursor()
		cursor.execute('SELECT COUNT(*) FROM usuarios WHERE user_id = ?', (user_id,))
		result = cursor.fetchone()[0]
		conn.close()
		if result > 0:
			return True
		else:
			return False
	def data_user(self,user_id):
		conn = sqlite3.connect('usuarios.db')
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM usuarios WHERE user_id = ?', (user_id,))
		result = cursor.fetchone()
		conn.close()
		if result is not None:
			return result
		else:
			return None
	def agg_new_user(self,user_id,plan):
		try:
			save = {"uclv":20*1073741824,"uo":30*1073741824,"basico":15*1073741824,"estandar":25*1073741824,"avanzado":50*1073741824,"premium":100*1073741824}
			datos = {"plan":plan,"limite":save[plan],"total": 0}
			data = json.dumps(datos)
			conn = sqlite3.connect('usuarios.db')
			cursor = conn.cursor()
			cursor.execute('''
				INSERT INTO usuarios (user_id, data)
				VALUES (?, ?)
			''', (user_id, data))
			conn.commit()
			conn.close()
			return True
		except Exception as e:
			print(e)
			return False
	def update_user(self,user_id, data):
		data = json.dumps(data)
		conn = sqlite3.connect('usuarios.db')
		cursor = conn.cursor()
		cursor.execute('''UPDATE usuarios SET data = ? WHERE user_id = ? ''', (data,user_id))
		conn.commit()
		conn.close()
		return
	def delete_user(self, user_id):
		conn = sqlite3.connect('usuarios.db')
		cursor = conn.cursor()
		cursor.execute(''' DELETE FROM usuarios WHERE user_id = ? ''', (user_id,))
		conn.commit()
		conn.close()
		return True
	def all_userid(self):
		conn = sqlite3.connect(self._DB)
		cursor = conn.cursor()
		cursor.execute("SELECT user_id FROM usuarios")
		user_ids = cursor.fetchall()
		conn.close()
		if user_ids:
			user_ids = [user_id[0] for user_id in user_ids]
			return user_ids
		else:
			return []