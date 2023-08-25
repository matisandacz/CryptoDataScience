import psycopg2

class PostgreSQLService:
	def __init__(self, database="postgres", user="postgres", password="pass123", host="127.0.0.1", port="5432"):
		self.database = database
		self.user = user
		self.password = password
		self.host = host
		self.port = port

	def connect(self):
		self.connection = psycopg2.connect(database = self.database, 
			user = self.user,
			password = self.password, 
			host = self.host, 
			port = self.port)

	def createDataCampTable(self):
		self.executeCommand("""CREATE TABLE IF NOT EXISTS datacamp_courses(
			            course_id SERIAL PRIMARY KEY,
			            course_name VARCHAR (50) UNIQUE NOT NULL,
			            course_instructor VARCHAR (100) NOT NULL,
			            topic VARCHAR (20) NOT NULL);
			            """)

	def executeCommands(self, commands):
		for command in commands:
			self.executeCommand(command)

	def executeCommand(self, command):
		try:
			cursor = self.connection.cursor()
			cursor.execute(command)
			self.connection.commit()
			cursor.close()
		except Exception as err:
			raise err	
		finally:
			self.handleErrorAndCloseConn(cursor)

	def handleErrorAndCloseConn(self, cursor):
		cursor.close()
		self.connection.close()

try:
	postgresService = PostgreSQLService()
	postgresService.connect()
	postgresService.createDataCampTable()
except Exception as err:
	print(err)