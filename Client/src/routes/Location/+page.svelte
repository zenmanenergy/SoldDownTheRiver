<!-- src/routes/Locations/+page.svelte -->
<script>
	import { onMount } from 'svelte';
	import { handleSave } from './handleSave.js';
	import { handleDelete } from './handleDelete.js';
	import { handleGet } from './handleGet.js';

	let LocationId = "";
	let City = "";
	let State = "";
	let Country = "";
	let Latitude = "";
	let Longitude = "";
	let formValid = false;
	let isLoading = true;

	async function setLocation(city, state, country, latitude, longitude) {
		City = city;
		State = state;
		Country = country;
		Latitude = latitude;
		Longitude = longitude;
	}

	$: {
		formValid = City && State && Country && Latitude && Longitude;
	}

	onMount(async () => {
		const urlParams = new URLSearchParams(window.location.search);
		LocationId = urlParams.get("LocationId") || "";
		if (LocationId) {
			handleGet(LocationId, setLocation);
		}
		console.log("LocationId", LocationId)
    	isLoading = false;
	});
</script>

<style>
	input:required:invalid {
		border: 1px solid red;
	}
	input:required:valid {
		border: 1px solid #ccc;
	}
</style>

{#if isLoading}
  <div class="loading-screen">
    <div class="spinner"></div>
  </div>
{:else}
	<div>
		<form>
			<h2>Add a Location</h2>

			<input type="hidden" bind:value={LocationId} />

			<div>
				<label for="City">City</label>
				<input
					type="text"
					id="City"
					placeholder="Enter City Name"
					bind:value={City}
					required
				/>
			</div>

			<div>
				<label for="State">State</label>
				<input
					type="text"
					id="State"
					placeholder="Enter State Name"
					bind:value={State}
					required
				/>
			</div>

			<div>
				<label for="Country">Country</label>
				<input
					type="text"
					id="Country"
					placeholder="Enter Country Name"
					bind:value={Country}
					required
				/>
			</div>

			<div>
				<label for="Latitude">Latitude</label>
				<input
					type="number"
					id="Latitude"
					placeholder="Enter Latitude"
					step="0.0001"
					bind:value={Latitude}
					required
				/>
			</div>

			<div>
				<label for="Longitude">Longitude</label>
				<input
					type="number"
					id="Longitude"
					placeholder="Enter Longitude"
					step="0.0001"
					bind:value={Longitude}
					required
				/>
			</div>

			<div>
				<button type="button" on:click={() => handleSave(LocationId, City, State, Country, Latitude, Longitude, formValid)}>Save</button>
				{#if LocationId.length}
					<button type="button" on:click={() => handleDelete(LocationId)}>Delete</button>
				{/if}
			</div>
		</form>
	</div>
{/if}
