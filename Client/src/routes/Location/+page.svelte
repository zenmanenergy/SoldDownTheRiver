
<!-- src/routes/Locations/+page.svelte -->
<style>
	@import "/static/FormPages.css";
</style>

<script>
	import moment from 'moment';
	import { onMount } from "svelte";
	import { handleSave } from "./handleSave.js";
	import { handleDelete } from "./handleDelete.js";
	import { handleGetLocation } from "./handleGetLocation.js";
	import {Session} from "../Session.js";

	let LastModified='';
	let LocationId = "";
	let City = "";
	let State = "";
	let Country = "";
	let Latitude = "";
	let Longitude = "";
	let formValid = false;
	let isLoading = true;
	let Location={LocationId :"", City : "", State : "", Country : "", Latitude : "", Longitude : "", LastModified : ""}

	async function setLocation(data) {
		Location.LocationId = data.LocationId || "";
		Location.City = data.City || "";
		Location.State = data.State || "";
		Location.Country = data.Country || "";
		Location.Latitude = data.Latitude || "";
		Location.Longitude = data.Longitude || "";
		Location.LastModified = data.LastModified || "";
		
	}

	$: {
		formValid = Location.City;
	}
	
	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		LocationId = urlParams.get("LocationId") || "";
		
		if (LocationId){
			
			await Promise.all([
				await handleGetLocation(Session.SessionId,LocationId, setLocation)
				
			]);
		}
		
		console.log("LocationId", LocationId);
		isLoading = false;
	});
</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner" />
	</div>
{:else}
	<div class="section">
		<a href="/Locations">Back to Locations</a>
		<div class="ActionBox">
			<form>
				<h3 class="title is-2">Edit a Location</h3>

				<input type="hidden" bind:value={Location.LocationId} />

				<div class="field">
					<label class="label" for="City">City</label>
					<div class="control">
						<input class="input" type="text" id="City" placeholder="Enter City Name" bind:value={Location.City} required />
					</div>
				</div>

				<div class="field">
					<label class="label" for="State">State</label>
					<div class="control">
						<input class="input" type="text" id="State" placeholder="Enter State Name" bind:value={Location.State}  />
					</div>
				</div>

				<div class="field">
					<label class="label" for="Country">Country</label>
					<div class="control">
						<input class="input" type="text" id="Country" placeholder="Enter Country Name" bind:value={Location.Country}  />
					</div>
				</div>

				<div class="field">
					<label class="label" for="Latitude">Latitude</label>
					<div class="control">
						<input class="input" type="number" id="Latitude" placeholder="Enter Latitude" step="0.0001" bind:value={Location.Latitude}  />
					</div>
				</div>

				<div class="field">
					<label class="label" for="Longitude">Longitude</label>
					<div class="control">
						<input class="input" type="number" id="Longitude" placeholder="Enter Longitude" step="0.0001" bind:value={Location.Longitude}  />
					</div>
				</div>

				<div class="field">
					<div class="control">
						<button class="button is-primary" on:click={() => handleSave(Session.SessionId,Location, formValid)}>Save</button>
						{#if LocationId.length}
							<button class="button is-danger" on:click={() => handleDelete(Session.SessionId,LocationId)}>Delete</button>
						{/if}
					</div>
				</div>
			</form>
			{#if LastModified}
				<small>Last Modified: {moment.utc(LastModified).local().fromNow()}</small>
			{/if}
		</div>
	</div>
{/if}
