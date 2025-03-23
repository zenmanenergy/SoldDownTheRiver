from _Lib import Database

def add_family_member(HumanId, RelatedHumanId, RelationshipType):
	cursor, connection = Database.ConnectToDatabase()

	def insert_parent_child(parent_id, child_id):
		# Insert direct relationship
		sql_insert_relationship = f"""
			INSERT IGNORE INTO humanrelationships (ParentHumanId, ChildHumanId)
			VALUES ('{parent_id}', '{child_id}')
		"""
		print("Executing SQL:", sql_insert_relationship)
		cursor.execute(sql_insert_relationship)
		connection.commit()

		# Insert direct humanclosure relationship (depth=1)
		sql_insert_closure_depth_1 = f"""
			INSERT IGNORE INTO humanclosure (AncestorHumanId, DescendantHumanId, Depth)
			VALUES ('{parent_id}', '{child_id}', 1)
		"""
		print("Executing SQL:", sql_insert_closure_depth_1)
		cursor.execute(sql_insert_closure_depth_1)
		connection.commit()

		# Insert all indirect ancestors (ancestors of parent → child)
		sql_insert_indirect_ancestors = f"""
			INSERT IGNORE INTO humanclosure (AncestorHumanId, DescendantHumanId, Depth)
			SELECT AncestorHumanId, '{child_id}', Depth + 1
			FROM humanclosure
			WHERE DescendantHumanId = '{parent_id}'
		"""
		print("Executing SQL:", sql_insert_indirect_ancestors)
		cursor.execute(sql_insert_indirect_ancestors)
		connection.commit()

		# Insert all indirect descendants (parent → descendants of child)
		sql_insert_indirect_descendants = f"""
			INSERT IGNORE INTO humanclosure (AncestorHumanId, DescendantHumanId, Depth)
			SELECT '{parent_id}', DescendantHumanId, Depth + 1
			FROM humanclosure
			WHERE AncestorHumanId = '{child_id}'
		"""
		print("Executing SQL:", sql_insert_indirect_descendants)
		cursor.execute(sql_insert_indirect_descendants)
		connection.commit()

		# Insert transitive humanrelationships (ancestors of parent → descendants of child)
		sql_insert_transitive_relationships = f"""
			INSERT IGNORE INTO humanclosure (AncestorHumanId, DescendantHumanId, Depth)
			SELECT c1.AncestorHumanId, c2.DescendantHumanId, c1.Depth + c2.Depth + 1
			FROM humanclosure c1
			JOIN humanclosure c2 ON c1.DescendantHumanId = '{parent_id}' AND c2.AncestorHumanId = '{child_id}'
		"""
		print("Executing SQL:", sql_insert_transitive_relationships)
		cursor.execute(sql_insert_transitive_relationships)
		connection.commit()

	if RelationshipType.lower() in ['son', 'daughter']:
		insert_parent_child(HumanId, RelatedHumanId)

	elif RelationshipType.lower() in ['father', 'mother']:
		insert_parent_child(RelatedHumanId, HumanId)

	elif RelationshipType.lower() in ['sister', 'brother']:
		# Retrieve all parents of HumanId
		sql_get_parents = f"""
			SELECT ParentHumanId FROM humanrelationships
			WHERE ChildHumanId = '{HumanId}'
		"""
		print("Executing SQL:", sql_get_parents)
		cursor.execute(sql_get_parents)
		parents = cursor.fetchall()
		for parent in parents:
			parent_id = parent['ParentHumanId']  # Access dict by key
			insert_parent_child(parent_id, RelatedHumanId)

		# Insert sibling relationship into humanrelationships
		sql_insert_sibling_relationship = f"""
			INSERT IGNORE INTO humanrelationships (ParentHumanId, ChildHumanId)
			SELECT ParentHumanId, '{RelatedHumanId}'
			FROM humanrelationships
			WHERE ChildHumanId = '{HumanId}'
		"""
		print("Executing SQL:", sql_insert_sibling_relationship)
		cursor.execute(sql_insert_sibling_relationship)
		connection.commit()

	elif RelationshipType.lower() in ['husband', 'wife']:
		# Spouse humanrelationships are not part of the humanclosure table
		sql_update_spouse_1 = f"""
			UPDATE humans
			SET spouseHumanId = '{RelatedHumanId}'
			WHERE HumanId = '{HumanId}'
		"""
		print("Executing SQL:", sql_update_spouse_1)
		cursor.execute(sql_update_spouse_1)

		sql_update_spouse_2 = f"""
			UPDATE humans
			SET spouseHumanId = '{HumanId}'
			WHERE HumanId = '{RelatedHumanId}'
		"""
		print("Executing SQL:", sql_update_spouse_2)
		cursor.execute(sql_update_spouse_2)
		connection.commit()

	# Update Sex field if it is NULL
	if RelationshipType.lower() in ['husband', 'son', 'brother', 'father']:
		sql_update_sex_male = f"""
			UPDATE humans
			SET sex = 'Male'
			WHERE HumanId = '{RelatedHumanId}' AND sex IS NULL
		"""
		print("Executing SQL:", sql_update_sex_male)
		cursor.execute(sql_update_sex_male)
		connection.commit()
	elif RelationshipType.lower() in ['wife', 'daughter', 'sister', 'mother']:
		sql_update_sex_female = f"""
			UPDATE humans
			SET sex = 'Female'
			WHERE HumanId = '{RelatedHumanId}' AND sex IS NULL
		"""
		print("Executing SQL:", sql_update_sex_female)
		cursor.execute(sql_update_sex_female)
		connection.commit()

	connection.commit()
	return {"success": True, "message": "Relationship saved successfully."}
