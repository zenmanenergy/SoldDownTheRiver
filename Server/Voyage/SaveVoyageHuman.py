import uuid
from _Lib import Database
import datetime

def save_VoyageHuman(VoyageId, HumanId, RoleId, owner_humanid,owner2_humanid,shippingagent_humanid,collectoragent_HumanId,Notes):
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()
	
	query = "INSERT into voyagehumans (VoyageId, HumanId, RoleId, owner_humanid, owner2_humanid, shippingagent_humanid, collectoragent_HumanId, Notes, DateUpdated)"
	query += f" VALUES ('{VoyageId}', '{HumanId}', '{RoleId}', '{owner_humanid}', '{owner2_humanid}', '{shippingagent_humanid}', '{collectoragent_HumanId}', '{Notes}', NOW())"
	query += " ON DUPLICATE KEY update voyageId=values(VoyageId), HumanId=values(HumanId), RoleId=values(RoleId), owner_humanid=values(owner_humanid), owner2_humanid=values(owner2_humanid), shippingagent_humanid=values(shippingagent_humanid), collectoragent_HumanId=values(collectoragent_HumanId), Notes=values(Notes), DateUpdated=NOW()"
		
	print(query )

	# Execute the query and commit the changes
	cursor.execute(query)
	connection.commit()

	# Close the database connection 
	connection.close()

	# Return the VoyageId as a JSON response
	return {'success': True, 'VoyageId:HumanId': VoyageId+":"+HumanId}
