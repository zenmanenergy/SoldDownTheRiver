from Lib import Database

def get_locations():
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT *, (select max(dateAdded) from History where History.KeyValue=Locations.LocationId  and History.TableName='Locations' and History.KeyName='LocationId') LastModified"
	query +="   FROM Locations order by City"
	# query +=" limit 50"
	values = ()


	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchall()
	if not result:
		result=[]
		
	# Close the database connection
	connection.close()
	
	
	return result
