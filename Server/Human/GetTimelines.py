from _Lib import Database

def get_timelines(HumanId):
	cursor, connection = Database.ConnectToDatabase()
	try:
		# Query the database for timelines related to the given HumanId, including location details
		query = """
			SELECT ht.LocationId, ht.Date_Circa, ht.Date_Accuracy, ht.LocationType,ht.RoleId,
				l.Address, l.City, l.County, l.State, l.State_abbr, 
				l.Country, l.Latitude, l.Longitude, l.LocationType
			FROM humantimeline ht
			LEFT JOIN locations l ON ht.LocationId = l.LocationId
			WHERE ht.HumanId = %s
			ORDER BY ht.Date_Circa ASC
		"""
		cursor.execute(query, (HumanId,))
		result = cursor.fetchall()  # Already returns a dictionary due to DictCursor

		# Close the database connection
		connection.close()

		return {"success": True, "data": result}
	except Exception as e:
		return {"success": False, "error": str(e)}
