import uuid
from _Lib import Database
import datetime

def save_transactionhuman(
	TransactionId, HumanId, Price, Notes, FirstName, MiddleName, LastName, BirthDate,
	BirthDateAccuracy, BirthPlace, RacialDescriptor, Sex, Height_cm, physical_features, profession
):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Ensure HumanId is valid
	if not HumanId:
		HumanId = "HUM" + str(uuid.uuid4())

	# Ensure BirthDate is a valid datetime format
	if BirthDate:
		if BirthDateAccuracy == "Y":  # Year Only → Default to January 1st
			BirthDate = f"{BirthDate}-01-01"
		elif BirthDateAccuracy == "M":  # Year-Month Only → Default to 1st day of the month
			BirthDate = f"{BirthDate}-01"

		try:
			# Convert to valid datetime format
			BirthDate = datetime.datetime.strptime(BirthDate, "%Y-%m-%d")
		except ValueError:
			BirthDate = None  # If conversion fails, store NULL
	else:
		BirthDate = None  # Ensure NULL if empty

	# Ensure Height_cm is a float (or NULL if invalid)
	try:
		Height_cm = float(Height_cm) if Height_cm else None
	except ValueError:
		Height_cm = None  # Store NULL if invalid

	# Ensure Price is a float (or NULL if invalid)
	try:
		Price = float(Price) if Price else None
	except ValueError:
		Price = None  # Store NULL if invalid

	# Insert or update the human record
	human_query = """
		INSERT INTO humans (
			HumanId, FirstName, MiddleName, LastName, BirthDate, BirthDateAccuracy, 
			BirthPlace, RacialDescriptor, Sex, Height_cm, physical_features, profession, DateUpdated
		) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
		ON DUPLICATE KEY UPDATE 
			FirstName=VALUES(FirstName), MiddleName=VALUES(MiddleName), LastName=VALUES(LastName),
			BirthDate=VALUES(BirthDate), BirthDateAccuracy=VALUES(BirthDateAccuracy),
			BirthPlace=VALUES(BirthPlace), RacialDescriptor=VALUES(RacialDescriptor),
			Sex=VALUES(Sex), Height_cm=VALUES(Height_cm),
			physical_features=VALUES(physical_features), profession=VALUES(profession),
			DateUpdated=NOW()
	"""

	human_values = (
		HumanId, FirstName, MiddleName, LastName, BirthDate, BirthDateAccuracy, BirthPlace,
		RacialDescriptor, Sex, Height_cm, physical_features, profession
	)

	cursor.execute(human_query, human_values)

	# Insert or update the transaction-human relationship
	relationship_query = """
		INSERT INTO transactionhumans (TransactionId, HumanId, Price, Notes)
		VALUES (%s, %s, %s, %s)
		ON DUPLICATE KEY UPDATE
			TransactionId=VALUES(TransactionId),
			HumanId=VALUES(HumanId),
			Price=VALUES(Price),
			Notes=VALUES(Notes)
	"""

	relationship_values = (TransactionId, HumanId, Price, Notes)

	cursor.execute(relationship_query, relationship_values)
	connection.commit()

	# Fetch the updated human record
	cursor.execute("SELECT * FROM humans WHERE HumanId = %s", (HumanId,))
	human_result = cursor.fetchone()

	# Close the database connection
	connection.close()

	# Return the full human data for immediate frontend update
	return human_result
