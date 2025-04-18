import uuid
from _Lib import Database
import datetime

def save_VoyageHuman(VoyageId, HumanId, RoleId, SellingSlaveTraderHumanId,BuyingSlaveTraderHumanId,ShippingAgentHumanId,CollectingAgentHumanId,Notes):
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()
	
	query = "INSERT into voyagehumans (VoyageId, HumanId, RoleId, SellingSlaveTraderHumanId, BuyingSlaveTraderHumanId, ShippingAgentHumanId, CollectingAgentHumanId, Notes, DateUpdated)"
	query += f" VALUES ('{VoyageId}', '{HumanId}', '{RoleId}', '{SellingSlaveTraderHumanId}', '{BuyingSlaveTraderHumanId}', '{ShippingAgentHumanId}', '{CollectingAgentHumanId}', '{Notes}', NOW())"
	query += " ON DUPLICATE KEY update voyageId=values(VoyageId), HumanId=values(HumanId), RoleId=values(RoleId), SellingSlaveTraderHumanId=values(SellingSlaveTraderHumanId), BuyingSlaveTraderHumanId=values(BuyingSlaveTraderHumanId), ShippingAgentHumanId=values(ShippingAgentHumanId), CollectingAgentHumanId=values(CollectingAgentHumanId), Notes=values(Notes), DateUpdated=NOW()"
		
	print(query )

	# Execute the query and commit the changes
	cursor.execute(query)
	connection.commit()

	# Close the database connection 
	connection.close()

	# Return the VoyageId as a JSON response
	return {'success': True, 'VoyageId:HumanId': VoyageId+":"+HumanId}
