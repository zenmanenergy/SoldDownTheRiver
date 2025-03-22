from _Lib import Database
import uuid

def add_family_member(HumanId, RelatedHumanId, RelationshipType):
	cursor, connection = Database.ConnectToDatabase()

	# Check if HumanId is already in a family
	cursor.execute(f"SELECT FamilyId FROM familymembers WHERE HumanId = '{HumanId}'")
	family_row = cursor.fetchone()

	if family_row:
		FamilyId = family_row['FamilyId']
	else:
		# Check if the family already exists before inserting
		cursor.execute(f"""
			SELECT FamilyId
			FROM families
			WHERE FamilyId = 'FAM{str(uuid.uuid4())}'
		""")
		existing_family = cursor.fetchone()

		if not existing_family:
			# Insert a new family record
			FamilyId = "FAM"+str(uuid.uuid4())
			cursor.execute(f"INSERT INTO families (FamilyId, FamilyName) VALUES ('{FamilyId}', 'New Family')")

			# Add HumanId to the new family
			cursor.execute(f"""
				INSERT INTO familymembers (HumanId, FamilyId, left_value, right_value)
				VALUES ('{HumanId}', '{FamilyId}', 1, 2)
			""")

	# Handle specific relationships with left_value and right_value calculations
	if RelationshipType.lower() in ['Son', 'Daughter']:
		# Check for duplicate child entry
		cursor.execute(f"""
			SELECT 1
			FROM familymembers
			WHERE HumanId = '{HumanId}' AND FamilyId = '{FamilyId}'
		""")
		existing_member = cursor.fetchone()

		if not existing_member:
			# Assign left_value and right_value as children of RelatedHumanId
			cursor.execute(f"""
				SELECT right_value
				FROM familymembers
				WHERE HumanId = '{RelatedHumanId}'
			""")
			parent_right = cursor.fetchone()['right_value']

			# Shift existing values to make space for the new child
			cursor.execute(f"""
				UPDATE familymembers
				SET right_value = right_value + 2
				WHERE FamilyId = '{FamilyId}' AND right_value >= {parent_right}
			""")
			cursor.execute(f"""
				UPDATE familymembers
				SET left_value = left_value + 2
				WHERE FamilyId = '{FamilyId}' AND left_value > {parent_right}
			""")

			# Insert the new family member
			cursor.execute(f"""
				INSERT INTO familymembers (HumanId, FamilyId, left_value, right_value)
				VALUES ('{HumanId}', '{FamilyId}', {parent_right}, {parent_right + 1})
			""")
	elif RelationshipType.lower() in ['Father', 'Mother']:
		# Check for duplicate parent entry
		cursor.execute(f"""
			SELECT 1
			FROM familymembers
			WHERE HumanId = '{HumanId}' AND FamilyId = '{FamilyId}'
		""")
		existing_member = cursor.fetchone()

		if not existing_member:
			# Assign left_value and right_value as parents of RelatedHumanId
			cursor.execute(f"""
				SELECT left_value
				FROM familymembers
				WHERE HumanId = '{RelatedHumanId}'
			""")
			child_left = cursor.fetchone()['left_value']

			# Shift existing values to make space for the new parent
			cursor.execute(f"""
				UPDATE familymembers
				SET right_value = right_value + 2
				WHERE FamilyId = '{FamilyId}' AND right_value >= {child_left}
			""")
			cursor.execute(f"""
				UPDATE familymembers
				SET left_value = left_value + 2
				WHERE FamilyId = '{FamilyId}' AND left_value >= {child_left}
			""")

			# Insert the new family member
			cursor.execute(f"""
				INSERT INTO familymembers (HumanId, FamilyId, left_value, right_value)
				VALUES ('{HumanId}', '{FamilyId}', {child_left - 2}, {child_left - 1})
			""")
	elif RelationshipType.lower() in ['Husband', 'Wife']:
		# Check for duplicate spouse entry
		cursor.execute(f"""
			SELECT 1
			FROM humans
			WHERE HumanId = '{HumanId}' AND spouseHumanId = '{RelatedHumanId}'
		""")
		existing_spouse = cursor.fetchone()

		if not existing_spouse:
			cursor.execute(f"""
				UPDATE humans
				SET spouseHumanId = '{RelatedHumanId}'
				WHERE HumanId = '{HumanId}'
			""")
	else:
		# Default case for other relationships
		cursor.execute(f"""
			SELECT 1
			FROM familymembers
			WHERE HumanId = '{RelatedHumanId}' AND FamilyId = '{FamilyId}'
		""")
		existing_member = cursor.fetchone()

		if not existing_member:
			cursor.execute(f"""
				SELECT MAX(right_value) AS max_right
				FROM familymembers
				WHERE FamilyId = '{FamilyId}'
			""")
			max_right = cursor.fetchone()['max_right'] or 0

			# Insert the new family member
			cursor.execute(f"""
				INSERT INTO familymembers (HumanId, FamilyId, left_value, right_value)
				VALUES ('{RelatedHumanId}', '{FamilyId}', {max_right + 1}, {max_right + 2})
			""")

	if RelationshipType.lower() in ['Son', 'Daughter', 'Father', 'Mother', 'Husband', 'Wife']:
		# Determine the sex based on the relationship type
		sex = None
		if RelationshipType.lower() in ['Son', 'Father', 'Husband']:
			sex = 'Male'
		elif RelationshipType.lower() in ['Daughter', 'Mother', 'Wife']:
			sex = 'Female'

		# Update the sex if it is currently null
		if sex:
			cursor.execute(f"""
				UPDATE humans
				SET Sex = '{sex}'
				WHERE HumanId = '{HumanId}' AND (Sex IS NULL OR Sex = '')
			""")

	# Update the family name based on the oldest member
	cursor.execute(f"""
		SELECT h.HumanId, h.FirstName, h.LastName, h.BirthDate
		FROM familymembers fm
		JOIN humans h ON fm.HumanId = h.HumanId
		WHERE fm.FamilyId = '{FamilyId}'
		ORDER BY h.BirthDate ASC
		LIMIT 1
	""")
	oldest_member = cursor.fetchone()

	if oldest_member:
		first_name = oldest_member['FirstName'] or ""
		last_name = oldest_member['LastName'] or ""
		birth_date = oldest_member['BirthDate'].strftime('%Y-%m-%d') if oldest_member['BirthDate'] else ""
		oldest_name = f"{first_name} {last_name} {birth_date}"
		oldest_name = oldest_name.replace("  ", " ")
		cursor.execute(f"""
			UPDATE families
			SET FamilyName = '{oldest_name}'
			WHERE FamilyId = '{FamilyId}'
		""")

	# Commit the transaction
	connection.commit()
	return {"success": True, "message": "Relationship saved successfully."}
# except Exception as e:
# 	connection.rollback()
# 	return {"success": False, "error": str(e)}
# finally:
# 	connection.close()
