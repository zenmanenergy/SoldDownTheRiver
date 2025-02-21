from _Lib import Database

def get_location(LocationId):
	if not LocationId:
		LocationId="-1"
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT *, (select max(dateAdded) from history where history.KeyValue=locations.LocationId  and history.TableName='locations' and history.KeyName='LocationId') LastModified"
	query +="  from locations WHERE LocationId = %s"
	values = (LocationId,)


	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchone()
	if not result:
		result={}
		
	# Close the database connection
	connection.close()
	
	# Return the result as a dictionary
	return result
