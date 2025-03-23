from _Lib import Database

def remove_family_member(HumanId, RelatedHumanId):
	cursor, connection = Database.ConnectToDatabase()

	def delete_parent_child(parent_id, child_id):
		# Remove direct relationship
		sql_delete_relationship = f"""
			DELETE FROM humanrelationships
			WHERE ParentHumanId = '{parent_id}' AND ChildHumanId = '{child_id}'
		"""
		print("Executing SQL:", sql_delete_relationship)
		cursor.execute(sql_delete_relationship)
		connection.commit()

		# Remove from humanclosure where depth=1
		sql_delete_closure_depth_1 = f"""
			DELETE FROM humanclosure
			WHERE AncestorHumanId = '{parent_id}' AND DescendantHumanId = '{child_id}' AND Depth = 1
		"""
		print("Executing SQL:", sql_delete_closure_depth_1)
		cursor.execute(sql_delete_closure_depth_1)
		connection.commit()

		# Remove indirect relationships where ancestor-descendant link passes through this relationship.
		# Use a subquery to avoid the MySQL 1093 error.
		sql_delete_indirect_relationships = f"""
			DELETE FROM humanclosure
			WHERE (AncestorHumanId, DescendantHumanId) IN (
				SELECT AncestorHumanId, DescendantHumanId
				FROM (
					SELECT c1.AncestorHumanId, c2.DescendantHumanId
					FROM humanclosure c1
					JOIN humanclosure c2 ON c1.DescendantHumanId = '{parent_id}' AND c2.AncestorHumanId = '{child_id}'
				) AS temp_subquery
			)
		"""
		print("Executing SQL:", sql_delete_indirect_relationships)
		cursor.execute(sql_delete_indirect_relationships)
		connection.commit()

	def delete_sibling_relationship(human_id, sibling_id):
		# Use a temporary table or subquery to avoid the MySQL 1093 error
		sql_create_temp_table = f"""
			CREATE TEMPORARY TABLE temp_sibling_relationships AS
			SELECT ParentHumanId
			FROM humanrelationships
			WHERE ChildHumanId = '{human_id}'
		"""
		print("Executing SQL:", sql_create_temp_table)
		cursor.execute(sql_create_temp_table)

		sql_delete_sibling_relationship = f"""
			DELETE FROM humanrelationships
			WHERE ParentHumanId IN (SELECT ParentHumanId FROM temp_sibling_relationships)
			AND ChildHumanId = '{sibling_id}'
		"""
		print("Executing SQL:", sql_delete_sibling_relationship)
		cursor.execute(sql_delete_sibling_relationship)
		connection.commit()

		# Drop the temporary table
		sql_drop_temp_table = "DROP TEMPORARY TABLE temp_sibling_relationships"
		print("Executing SQL:", sql_drop_temp_table)
		cursor.execute(sql_drop_temp_table)

	# Determine the type of relationship and handle accordingly
	if RelatedHumanId and HumanId:
		# Check if the relationship is a sibling
		cursor.execute(f"""
			SELECT COUNT(*) AS count
			FROM humanrelationships r1
			JOIN humanrelationships r2 ON r1.ParentHumanId = r2.ParentHumanId
			WHERE r1.ChildHumanId = '{HumanId}' AND r2.ChildHumanId = '{RelatedHumanId}'
		""")
		result = cursor.fetchone()
		if result and result['count'] > 0:
			# Handle sibling relationship
			delete_sibling_relationship(HumanId, RelatedHumanId)
		else:
			# Handle parent-child relationship
			delete_parent_child(HumanId, RelatedHumanId)
			delete_parent_child(RelatedHumanId, HumanId)

		return {"success": True, "message": "Relationship removed successfully."}
	else:
		return {"failure": True, "message": "Relationship removal failed. Missing RelatedHumanId and HumanId"}
