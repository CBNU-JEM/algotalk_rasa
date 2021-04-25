import pymysql

debug = True

db = pymysql.connect(host = 'localhost', user = 'algotalk', password = 'algojem', db = 'algotalk_db', autocommit = True, sql_mode = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION')
cur = db.cursor()
cur.execute('set @@auto_increment_increment=1')

class Algorithm:
	def __init__(self, name = None, brief_explain = None, detail_explain = None, level = None, example_code = None):
		self.name = name
		self.brief_explain = brief_explain
		self.detail_explain = detail_explain
		self.level = level
		self.example_code = example_code
