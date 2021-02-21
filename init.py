from mysql.connector import connect, Error

create_db_query = """
CREATE DATABASE IF NOT EXISTS tripdb
"""

def getConnection():
  try:
    connection = connect( 
      host="localhost",
      user='root',
      password="123456",
    )
  except Error as e:    
    print(e)
  return connection

def executeQuery(query,connection):
  try:
    with connection.cursor() as cursor:
      cursor.execute(query)
      connection.commit()
      for abc in cursor:
        print(abc)
  except Error as e:
    print(e)

def main():
  connection = getConnection()
  executeQuery('DROP DATABASE tripdb', connection)
  executeQuery(create_db_query,connection)
main()