<!-- src/routes/Businesses/+page.svelte -->
<script>
	import { onMount } from 'svelte';
	import { handleSave } from './handleSave.js';
	import { handleDelete } from './handleDelete.js';
	import { handleGet } from './handleGet.js';

	let BusinessId="";
	let BusinessName = "";
	let formValid = false;
  	let isLoading = true;

	async function setName(newBusinessName) {
		BusinessName = newBusinessName;
	}

	$: {
		formValid = BusinessName;
	}
	onMount(async () => {
		const urlParams = new URLSearchParams(window.location.search);
		BusinessId = urlParams.get("BusinessId") || "";
		if (BusinessId) {
			handleGet(BusinessId, setName);
		}
		console.log("BusinessId", BusinessId)
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
			<h2>Add a Business</h2>

			<input type="hidden" bind:value={BusinessId} />

			<div>
				<label for="BusinessName">Name</label>
				<input
					type="text"
					id="BusinessName"
					placeholder="Enter Business Name"
					bind:value={BusinessName}
					required
				/>
			</div>

			<div>
				<button type="button" on:click={() => handleSave(BusinessId, BusinessName,formValid)} >Save</button>
				{#if BusinessId.length}
					<button type="button" on:click={() => handleDelete(BusinessId)}>Delete</button>
				{/if}
			</div>
		</form>
	</div>
{/if}