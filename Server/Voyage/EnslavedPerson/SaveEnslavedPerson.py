import uuid
from _Lib import Database
import datetime

def save_EnslavedPerson(HumanId, RoleId, FirstName, MiddleName, LastName):
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()
	
	query = "INSERT into humans (VoyageId, HumanId, RoleId, SellingSlaveTraderHumanId,BuyingSlaveTraderHumanId,ShippingAgentHumanId,collectoragentHumanId,Notes, DateUpdated)"
	query += f" VALUES ('{VoyageId}', '{HumanId}','{RoleId}','{SellingSlaveTraderHumanId}', '{BuyingSlaveTraderHumanId}','{ShippingAgentHumanId}', '{collectoragentHumanId}','{Notes}', NOW())"
	query +=" ON DUPLICATE KEY update voyageId=values(VoyageId),HumanId=values(HumanId) ,RoleId=values(RoleId), "
	query += "SellingSlaveTraderHumanId=values(SellingSlaveTraderHumanId),BuyingSlaveTraderHumanId=values(BuyingSlaveTraderHumanId),"
	query += "ShippingAgentHumanId=values(ShippingAgentHumanId),collectoragentHumanId=values(collectoragentHumanId),"
	query += "Notes=values(Notes), DateUpdated=NOW()"
		
	print(query )

	# Execute the query and commit the changes
	cursor.execute(query)
	connection.commit()

	# Close the database connection 
	connection.close()

	# Return the VoyageId as a JSON response
	return {'success': True, 'VoyageId:HumanId': VoyageId+":"+HumanId}
