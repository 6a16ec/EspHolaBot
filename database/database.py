import psycopg2

user = "espholabot"; password = "pass_Ghye74gh"; host = "127.0.0.1"; port = "5432"; database = "EspHolaBot"

class Database():
	def __init__(self, host=host, database=database, user=user, password=password):
		self.conn = psycopg2.connect(host=host, database=database, user=user, password=password)
		self.cur = self.conn.cursor()

	def query(self, query, args = None):
		need_commit = False
		if "create" in query.lower(): need_commit = True
		if "insert" in query.lower(): need_commit = True
		if "delete" in query.lower(): need_commit = True
		if "update" in query.lower(): need_commit = True

		if args:
			self.cur.execute(query, args)
		else:
			self.cur.execute(query)

		if need_commit: self.commit()

	def close(self):
		self.cur.close()
		self.conn.close()

	def commit(self):
		self.conn.commit()

	def data(self):
		return self.cur

if __name__ == "__main__":
	db = MyDatabase()
	# db.query("INSERT INTO profile_new VALUES ('0', 0, 0)")
	db.close()
