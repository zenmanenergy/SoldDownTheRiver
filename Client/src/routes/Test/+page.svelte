<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Select2 Integration</title>
	
	<!-- Include jQuery from CDN -->
	<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

	<!-- Include Select2 CSS and JS from CDN -->
	<link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />
	<script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>
</head>
<body>

	<!-- Your select element -->
	<select id="mySelect" style="width: 200px;"></select>

	<script>
		// Your JavaScript code from earlier

		function fetchData(query, callback) {
			// Assuming a GET request to an endpoint that returns a JSON array of items
			fetch(`https://api.example.com/items?query=${query}`)
				.then(response => response.json())
				.then(data => {
					let items = data.map(item => {
						return { id: item.id, text: item.name };
					});
					callback(items);
				})
				.catch(error => console.error("Error fetching data:", error));
		}

		$(document).ready(function() {
			$("#mySelect").select2({
				placeholder: "Search for a human...",
				minimumInputLength: 3, 
				ajax: {
					delay: 250,
					url: function (params) {
						return "/Humans/GetHumans";  // Your endpoint
					},
					dataType: 'json',
					data: function (params) {
						return {
							Query: params.term  // Search term
						};
					},
					processResults: function (data) {
						return {
							results: data.map(human => {
								let fullName = `${human.FirstName || ''} ${human.MiddleName || ''} ${human.LastName || ''}`.trim();
								return { id: human.HumanId, text: fullName };
							})
						};
					}
				}
			});

		});
	</script>

</body>
</html>
