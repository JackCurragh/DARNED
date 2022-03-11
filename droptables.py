import MySQLdb
conn = MySQLdb.connect(db='darned')
cursor = conn.cursor()

cursor.execute("show tables")
rows = cursor.fetchall()
for row in rows:
    cursor.execute("DROP TABLE IF EXISTS %s"%row[0])
