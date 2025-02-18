import requests

BASE_URL = "http://127.0.0.1:80"
LocationId = None  # Global variable to store LocationId


def test_insert_location():
	"""
	Test the /Location/SaveLocation route for inserting a new location.
	"""
	global LocationId

	params = {
		"SessionId": "1",
		"LocationId": "",
		"City": "Norfolk",
		"State": "VA",
		"Country": "USA",
		"Latitude": "36.8508",
		"Longitude": "-76.2859"
	}

	print("Testing /Location/SaveLocation (Insert)")
	print("Params:", params)
	response = requests.get(f"{BASE_URL}/Location/SaveLocation", params=params)
	response_data = response.json()
	print("Response:", response_data)

	# Save the LocationId from the response to the global variable
	global LocationId
	LocationId = response_data.get("LocationId")
	print("Saved LocationId to global variable:", LocationId)


def test_update_location():
	"""
	Test the /Location/SaveLocation route for updating an existing location.
	"""
	global LocationId

	params = {
		"SessionId": "1",
		"LocationId": LocationId,
		"City": "Updated Norfolk",
		"State": "VA",
		"Country": "USA",
		"Latitude": "36.8508",
		"Longitude": "-76.2859"
	}

	print("Testing /Location/SaveLocation (Update)")
	print("Params:", params)
	response = requests.get(f"{BASE_URL}/Location/SaveLocation", params=params)
	print("Response:", response.json())


def test_get_location():
	"""
	Test the /Location/GetLocation route with the global LocationId.
	"""
	global LocationId

	params = {
		"SessionId": "1",
		"LocationId": LocationId
	}

	print("Testing /Location/GetLocation")
	print("Params:", params)
	response = requests.get(f"{BASE_URL}/Location/GetLocation", params=params)
	print("Response:", response.json())


def test_delete_location():
	"""
	Test the /Location/DeleteLocation route with the global LocationId.
	"""
	global LocationId

	params = {
		"SessionId": "1",
		"LocationId": LocationId
	}

	print("Testing /Location/DeleteLocation")
	print("Params:", params)
	response = requests.get(f"{BASE_URL}/Location/DeleteLocation", params=params)
	print("Response:", response.json())


if __name__ == "__main__":
	print("Starting Tests...")

	# Step 1: Insert a new location
	test_insert_location()

	# Step 2: Update the location with the global LocationId
	test_update_location()

	# Step 3: Retrieve the location using the global LocationId
	test_get_location()

	# Step 4: Delete the location using the global LocationId
	test_delete_location()

	print("Tests Completed.")
