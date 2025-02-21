from _Lib import Database

def delete_VoyageHuman(VoyageId, HumanId):
	# Delete the specified row from the Voyages table
	query = f"DELETE from voyagehumans WHERE VoyageId = '{VoyageId}' and  HumanId = '{HumanId}'"
	cursor, connection = Database.ConnectToDatabase()
	cursor.execute(query)
	connection.commit()
	connection.close()

	return {'success': True,'message': f'Voyage with VoyageId {VoyageId} HumanId {HumanId} deleted successfully.'}
