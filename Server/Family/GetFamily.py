from _Lib import Database

def get_family(HumanId):
	if not HumanId:
		return []

	cursor, connection = Database.ConnectToDatabase()

	cursor.execute(f"""
		SELECT HumanId, FirstName, LastName, Sex
		FROM humans
		WHERE HumanId = '{HumanId}'
	""")
	human = cursor.fetchone()
	if not human:
		connection.close()
		return []

	family_tree = [{
		'HumanId': human['HumanId'],
		'FirstName': human['FirstName'],
		'LastName': human['LastName'],
		'Relationship': 'self',
		'Depth': 0
	}]

	cursor.execute(f"""
		SELECT 
			h.HumanId,
			h.FirstName,
			h.LastName,
			h.Sex,
			c.Depth,
			'ancestor' AS RelationType
		FROM humanclosure c
		JOIN humans h ON c.AncestorHumanId = h.HumanId
		WHERE c.DescendantHumanId = '{HumanId}' AND c.Depth > 0

		UNION ALL

		SELECT 
			h.HumanId,
			h.FirstName,
			h.LastName,
			h.Sex,
			c.Depth,
			'descendant' AS RelationType
		FROM humanclosure c
		JOIN humans h ON c.DescendantHumanId = h.HumanId
		WHERE c.AncestorHumanId = '{HumanId}' AND c.Depth > 0

		ORDER BY RelationType DESC, Depth ASC, LastName, FirstName;
	""")

	relatives = list(cursor.fetchall())

	cursor.execute(f"""
		SELECT DISTINCT
			h.HumanId,
			h.FirstName,
			h.LastName,
			h.Sex,
			0 AS Depth,
			'sibling' AS RelationType
		FROM humanrelationships r1
		JOIN humanrelationships r2 ON r1.ParentHumanId = r2.ParentHumanId
		JOIN humans h ON r2.ChildHumanId = h.HumanId
		WHERE r1.ChildHumanId = '{HumanId}'
		  AND r2.ChildHumanId != '{HumanId}';
	""")

	siblings = list(cursor.fetchall())

	connection.close()

	full_family = relatives + siblings

	for member in full_family:
		sex = member['Sex']
		relation = member['RelationType']
		depth = member['Depth']

		if relation == 'ancestor':
			# invert depth explicitly
			if depth == 1:
				relation_label = 'father' if sex == 'Male' else 'mother'
			elif depth == 2:
				relation_label = 'grandfather' if sex == 'Male' else 'grandmother'
			else:
				relation_label = f'{"great-" * (depth - 2)}{"grandfather" if sex == "Male" else "grandmother"}'

		elif relation == 'descendant':
			if depth == 1:
				relation_label = 'son' if sex == 'Male' else 'daughter'
			elif depth == 2:
				relation_label = 'grandson' if sex == 'Male' else 'granddaughter'
			else:
				relation_label = f'{"great-" * (depth - 2)}{"grandson" if sex == "Male" else "granddaughter"}'

		elif relation == 'sibling':
			relation_label = 'brother' if sex == 'Male' else 'sister'
			depth = 0

		else:
			relation_label = 'relative'

		# Explicitly invert ancestor depth here
		final_depth = -depth if relation == 'ancestor' else depth

		family_tree.append({
			'HumanId': member['HumanId'],
			'FirstName': member['FirstName'],
			'LastName': member['LastName'],
			'Relationship': relation_label,
			'Depth': final_depth
		})

	return family_tree
