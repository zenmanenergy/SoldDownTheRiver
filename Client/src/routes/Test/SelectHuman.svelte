<script>
	import { onMount } from "svelte";

	let humans = [];
	
	import { onMount } from "svelte";

onMount(async () => {
	const selectElement = document.querySelector("#human-select");
	
	// Fetch data using the Fetch API
	const response = await fetch("http://localhost:80/Humans/GetHumans?Query=abc");
	const data = await response.json();

	// Process the results
	const processedData = data.map(human => ({
		id: human.HumanId,
		text: `${human.FirstName || ''} ${human.MiddleName || ''} ${human.LastName || ''}`.trim()
	}));

	// Initialize select2 with fetched data
	$(selectElement).select2({
		data: processedData,
		placeholder: 'Select a human',
		minimumInputLength: 1
	});
});

</script>

<select id="human-select">
</select>
