from google.cloud import bigquery
from mysql.connector import connect, Error
import time
import threading, queue
import queries
import sys

q = queue.Queue()

def worker():
    connection = getConnection()
    while True:
        item = q.get()
        try:
          ### Do inserts
          dim_location_id = executeManyQuery(queries.insert_dim_location_query,[(item.pickup_location,item.dropoff_location)],connection)
          dim_time_id = executeManyQuery(queries.insert_dim_time_query,[(item.trip_start_timestamp,item.trip_end_timestamp,item.trip_seconds)],connection)
          dim_payment_id = executeManyQuery(queries.insert_dim_payment_query,[(item.payment_type,item.trip_total,item.fare,item.tips,item.tolls,item.extras)],connection) 
          executeManyQuery(queries.insert_dim_taxi_query,[(item.taxi_id,item.company)],connection)
          executeManyQuery(queries.insert_trips_query,[(item.unique_key,item.taxi_id,dim_time_id,dim_location_id,dim_payment_id,item.trip_miles)],connection)
      
        except Error as e:
          print(e)
        q.task_done()

start_time = time.time()

# BIGQUERY STUFF
def getClientData():
  # Construct a BigQuery client object.
  client = bigquery.Client()
  query = (f"""
  SELECT * FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips` 
  WHERE trip_start_timestamp BETWEEN '2017-01-01' AND '2018-01-01'
  ORDER BY trip_start_timestamp ASC
  LIMIT {rows}
  """)

  query_job = client.query(query)  # Make an API request.
  return query_job

def getConnection():
  try:
    connection = connect( 
      host="localhost",
      user='root',
      password="123456",
      database="tripdb"
    )
  except Error as e:    
    print(e)
  return connection

def executeQuery(query,connection):
  try:
    with connection.cursor() as cursor:
      cursor.execute(query)
      connection.commit()
      for result in cursor:
        print(result)
  except Error as e:
    if (verbose):
      print(e)
    else:
      pass
    pass

def executeManyQuery(query,data,connection):
  try:
    with connection.cursor() as cursor:
      cursor.executemany(query,data)
      connection.commit()
      row_id = (cursor.lastrowid)
      return row_id
  except Error as e:
    if (verbose):
      print(e)
    else:
      pass
    pass

def createTables():
  connection = getConnection()
  executeQuery(queries.create_table_dim_location,connection)
  executeQuery(queries.create_table_dim_time,connection)
  executeQuery(queries.create_table_dim_payment,connection)
  executeQuery(queries.create_table_dim_taxi,connection)
  executeQuery(queries.create_table_dim_trips,connection)

def main():
  # Create tables in case they don't exist
  createTables()
  
  # setup threads, although the real bottleneck is most likely internet speed
  num_fetch_threads = 15
  for i in range(num_fetch_threads):
    workerThread = threading.Thread(target=worker)
    workerThread.setDaemon(True)
    workerThread.start()
  
  # get data from BigQuery API
  query_job = getClientData()
  
  print("Processing rows...", query_job.state)
  
  for row in query_job: 
    # put each row into queue
    q.put(row)

  q.join()
  print('All work completed')
  print ("Time elapsed: ", time.time() - start_time)


if __name__ == "__main__":
  if (len(sys.argv) > 1):
    try:
      int(sys.argv[1])
    except ValueError:
      print("Please provide a number of rows to process!")
    global verbose
    global rows
    rows = sys.argv[1]
    if (len(sys.argv) > 2 and sys.argv[2] == "v"):
      verbose = True
    else:
      verbose = False
    main()
  else:
    print("Please provide a number of rows to process!")