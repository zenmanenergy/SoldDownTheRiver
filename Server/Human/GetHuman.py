from Lib import Database

def get_human(HumanId):
	if not HumanId:
		HumanId="-1"
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL sql
	sql = f"SELECT * , (select max(dateAdded) from History where History.KeyValue=Humans.HumanId and History.TableName='Humans' and History.KeyName='HumanId') LastModified"
	sql += f" FROM Humans WHERE Humans.HumanId = '{HumanId}'"
	
	print(sql)
	# Execute the sql and get the results
	cursor.execute(sql)
	result = cursor.fetchone()
	if not result:
		result={}
		
	# Close the database connection
	connection.close()
	
	# Return the result as a dictionary
	return result
