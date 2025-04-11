from _Lib import Database

def get_timelines(LocationId):
	cursor, connection = Database.ConnectToDatabase()
	try:
		# Query the database for timelines related to the given LocationId, including location details
		query = """
			SELECT h.HumanId, h.FirstName, h.LastName, ht.Date_Circa, ht.Date_Accuracy, ht.LocationId, ht.RoleId, ht.Date_Circa, ht.Date_Accuracy, ht.LocationType,
				l.Address, l.City, l.County, l.State, l.State_abbr, 
				l.Country, l.Latitude, l.Longitude, l.LocationType
			FROM locations l join humantimeline ht ON ht.LocationId = l.LocationId
			join humans h on ht.HumanId=h.HumanId
			WHERE l.LocationId = %s
			ORDER BY ht.Date_Circa ASC
		"""
		cursor.execute(query, (LocationId,))
		result = cursor.fetchall()  # Already returns a dictionary due to DictCursor

		# Close the database connection
		connection.close()

		return {"success": True, "data": result}
	except Exception as e:
		return {"success": False, "error": str(e)}
