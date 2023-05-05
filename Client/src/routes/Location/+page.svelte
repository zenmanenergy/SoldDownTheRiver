
<!-- src/routes/Locations/+page.svelte -->
<style>
	@import "/static/FormPages.css";
</style>

<script>
	import moment from 'moment';
	import { onMount } from "svelte";
	import { handleSave } from "./handleSave.js";
	import { handleDelete } from "./handleDelete.js";
	import { handleGet } from "./handleGet.js";
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

	async function setLocation(city, state, country, latitude, longitude, lastModified) {
		City = city;
		State = state;
		Country = country;
		Latitude = latitude;
		Longitude = longitude;
		LastModified = lastModified;
	}

	$: {
		formValid = City;
	}

	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		LocationId = urlParams.get("LocationId") || "";
		
		if (LocationId){
			handleGet(Session.SessionId,LocationId, setLocation);
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

				<input type="hidden" bind:value={LocationId} />

				<div class="field">
					<label class="label" for="City">City</label>
					<div class="control">
						<input type="text" id="City" placeholder="Enter City Name" bind:value={City} required />
					</div>
				</div>

				<div class="field">
					<label class="label" for="State">State</label>
					<div class="control">
						<input type="text" id="State" placeholder="Enter State Name" bind:value={State}  />
					</div>
				</div>

				<div class="field">
					<label class="label" for="Country">Country</label>
					<div class="control">
						<input type="text" id="Country" placeholder="Enter Country Name" bind:value={Country}  />
					</div>
				</div>

				<div class="field">
					<label class="label" for="Latitude">Latitude</label>
					<div class="control">
						<input type="number" id="Latitude" placeholder="Enter Latitude" step="0.0001" bind:value={Latitude}  />
					</div>
				</div>

				<div class="field">
					<label class="label" for="Longitude">Longitude</label>
					<div class="control">
						<input type="number" id="Longitude" placeholder="Enter Longitude" step="0.0001" bind:value={Longitude}  />
					</div>
				</div>

				<div class="field">
					<div class="control">
						<button type="button" on:click={() => handleSave(Session.SessionId,LocationId, City, State, Country, Latitude, Longitude, formValid)}>Save</button>
						{#if LocationId.length}
							<button type="button" on:click={() => handleDelete(Session.SessionId,LocationId)}>Delete</button>
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
