from _Lib import Database

def get_locations():
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT *, (select max(dateAdded) from history where history.KeyValue=locations.LocationId  and history.TableName='locations' and history.KeyName='LocationId') LastModified"
	query +="   from locations order by City"
	values = ()

	# print(query)

	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchall()
	if not result:
		result=[]
		
	# Close the database connection
	connection.close()
	
	
	return result

