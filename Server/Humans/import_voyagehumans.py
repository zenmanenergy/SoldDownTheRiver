from _Lib.Database import ConnectToDatabase
import uuid
from datetime import datetime

def import_voyagehumans():
	# Connect to the database
	cursor, connection = ConnectToDatabase()

	# Fetch records from raw_manifest where shipvoyageid and enslaved_humanid are not null
	query = """
		SELECT shipvoyageid, enslaved_humanid, manifest_id, Owner_humanId, ShippingAgent_humanId, 
		       Owner2_humanId, CollectorAgent_humanId
		FROM raw_manifest
		WHERE shipvoyageid IS NOT NULL AND enslaved_humanid IS NOT NULL
		
	"""
	print(query)
	cursor.execute(query)
	raw_manifest_records = cursor.fetchall()

	# Process each record
	for record in raw_manifest_records:
		shipvoyageid = record["shipvoyageid"]
		enslaved_humanid = record["enslaved_humanid"]
		manifest_id = record["manifest_id"]
		owner_humanid = record["Owner_humanId"]
		shippingagent_humanid = record["ShippingAgent_humanId"]
		owner2_humanid = record["Owner2_humanId"]
		collectoragent_humanid = record["CollectorAgent_humanId"]

		# Generate the SQL statement to update voyagehumans
		update_query = f"""
			UPDATE voyagehumans
			SET manifest_id = {f"'{manifest_id}'" if manifest_id else 'NULL'},
				owner_humanid = {f"'{owner_humanid}'" if owner_humanid else 'NULL'},
				shippingagent_humanid = {f"'{shippingagent_humanid}'" if shippingagent_humanid else 'NULL'},
				owner2_humanid = {f"'{owner2_humanid}'" if owner2_humanid else 'NULL'},
				collectoragent_humanid = {f"'{collectoragent_humanid}'" if collectoragent_humanid else 'NULL'}
			WHERE VoyageId = '{shipvoyageid}' AND HumanId = '{enslaved_humanid}';
		"""
		print(update_query)  # Print the query for verification

	# Close the database connection
	connection.close()

	return "done"