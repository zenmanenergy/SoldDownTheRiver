from _Lib import Database

def get_BusinessHumans(BusinessId):

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT *, (select max(dateAdded) from history where history.KeyValue=humans.HumanId and history.TableName='humans' and history.KeyName='HumanId') LastModified"
	query +=" from humans join businesshumans on humans.HumanId=businesshumans.HumanId "
	query +=" join roles on businesshumans.RoleId=roles.RoleId "
	query +=" where businesshumans.BusinessId= %s "
	query +=" order by humans.LastName, humans.FirstName"
	values = (BusinessId,)

	print(query % values)
	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchall()
	if not result:
		result=[]
		
	# Close the database connection
	connection.close()

	# Return the result as a dictionary
	return result