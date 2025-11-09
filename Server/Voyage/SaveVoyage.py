import uuid
from _Lib import Database

def save_Voyage(VoyageId, ShipId, CaptainHumanId,StartLocationId, EndLocationId, StartDate, EndDate, Notes, isApproved=False):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	if len(StartDate) == 0:
		StartDate = None
	if len(EndDate) == 0:
		EndDate = None
	
	# Convert isApproved to boolean (ensure it's either 0 or 1)
	isApproved = 1 if str(isApproved).lower() in ["true", "1", "yes"] else 0
	# Check if the VoyageId is present
	if VoyageId:
		# If the VoyageId is present, update the existing Voyage
		query = "update voyages SET ShipId = %s, CaptainHumanId=%s, StartLocationId = %s, EndLocationId = %s, StartDate = %s, EndDate = %s, Notes = %s, isApproved = %s, DateUpdated = NOW() WHERE VoyageId = %s"
		values = (ShipId,CaptainHumanId, StartLocationId, EndLocationId, StartDate, EndDate, Notes, isApproved, VoyageId)
	else:
		# If the VoyageId is not present, create a new Voyage
		VoyageId = "VYG" + str(uuid.uuid4())
		query = "INSERT into voyages (VoyageId, ShipId,CaptainHumanId, StartLocationId, EndLocationId, StartDate, EndDate, Notes, isApproved, DateUpdated) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, NOW())"
		values = (VoyageId, ShipId,CaptainHumanId, StartLocationId, EndLocationId, StartDate, EndDate, Notes, isApproved)

	# Execute the query and commit the changes
	print(query, values)
	cursor.execute(query, values)
	
	# Update the isApproved status for the start location
	if StartLocationId:
		start_location_query = "UPDATE locations SET isApproved=%s WHERE LocationId=%s"
		start_location_params = (isApproved, StartLocationId)
		print("Executing Start Location SQL:\n" + start_location_query + "\nWith params:\n" + str(start_location_params) + "\n")
		cursor.execute(start_location_query, start_location_params)
	
	# Update the isApproved status for the end location
	if EndLocationId:
		end_location_query = "UPDATE locations SET isApproved=%s WHERE LocationId=%s"
		end_location_params = (isApproved, EndLocationId)
		print("Executing End Location SQL:\n" + end_location_query + "\nWith params:\n" + str(end_location_params) + "\n")
		cursor.execute(end_location_query, end_location_params)
	
	# Update the isApproved status for the ship
	if ShipId:
		ship_query = "UPDATE ships SET isApproved=%s WHERE ShipId=%s"
		ship_params = (isApproved, ShipId)
		print("Executing Ship SQL:\n" + ship_query + "\nWith params:\n" + str(ship_params) + "\n")
		cursor.execute(ship_query, ship_params)
	
	# Update the isApproved status for humans associated with this voyage
	human_query = """UPDATE humans SET isApproved=%s 
					WHERE HumanId IN (
						SELECT HumanId FROM voyagehumans 
						WHERE VoyageId=%s
					)"""
	human_params = (isApproved, VoyageId)
	print("Executing Human SQL:\n" + human_query + "\nWith params:\n" + str(human_params) + "\n")
	cursor.execute(human_query, human_params)
	
	# Update locations based on humantimeline table for humans associated with this voyage
	timeline_location_query = """UPDATE locations 
								SET isApproved=%s 
								WHERE LocationId IN (
									SELECT t.LocationId FROM humantimeline t 
									JOIN humans h ON h.HumanId = t.HumanId 
									JOIN voyagehumans vh ON vh.HumanId = h.HumanId
									WHERE vh.VoyageId=%s
								)"""
	timeline_location_params = (isApproved, VoyageId)
	print("Executing Timeline Location SQL:\n" + timeline_location_query + "\nWith params:\n" + str(timeline_location_params) + "\n")
	cursor.execute(timeline_location_query, timeline_location_params)
	
	connection.commit()

	# Close the database connection
	connection.close()

	# Return the VoyageId as a JSON response
	return {'success': True, 'VoyageId': VoyageId, 'EndDate': EndDate}
