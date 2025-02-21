<style>
	@import '/static/FormPages.css';
</style>

<script>
	import { onMount } from 'svelte';
	import { handleSaveNOLA } from './handleSaveNOLA.js';
	import { handleDeleteNOLA } from './handleDeleteNOLA.js';
	import { Session } from "../Session.js";
	import { handleGetNOLA } from './handleGetNOLA.js';

	let formValid = false;
	let isLoading = true;
	let NOLA = {
		NOLA_ID: "",
		FirstParty: "",
		LocationFirstParty: "",
		SecondParty: "",
		LocationSecondParty: "",
		TypeOfTransaction: "",
		DateOfTransaction: "",
		Act: "",
		Page: "",
		NotaryPublic: "",
		Volume: "",
		NameOfTranscriber: "",
		ReferenceURL: ""
	};

	async function setNOLA(data) {
		NOLA = {  // Reassign the entire object to trigger reactivity
			NOLA_ID: data.NOLA_ID || "",
			FirstParty: data.FirstParty || "",
			LocationFirstParty: data.LocationFirstParty || "",
			SecondParty: data.SecondParty || "",
			LocationSecondParty: data.LocationSecondParty || "",
			TypeOfTransaction: data.TypeOfTransaction || "",
			DateOfTransaction: data.DateOfTransaction || "",
			Act: data.Act || "",
			Page: data.Page || "",
			NotaryPublic: data.NotaryPublic || "",
			Volume: data.Volume || "",
			NameOfTranscriber: data.NameOfTranscriber || "",
			ReferenceURL: data.ReferenceURL || ""
		};
	}



	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		NOLA.NOLA_ID = urlParams.get("NOLA_ID") || "";

		if (NOLA.NOLA_ID.trim() !== "") {
			await handleGetNOLA(Session.SessionId, NOLA.NOLA_ID, setNOLA);
		}
		
		isLoading = false;
	});


	async function confirmDelete() {
		const userConfirmed = confirm('Are you sure you want to delete this NOLA record?\n\nThis action cannot be undone.');
		if (userConfirmed) {
			await handleDeleteNOLA(Session.SessionId, NOLA.NOLA_ID);
		}
	}
</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner"></div>
	</div>
{:else}
	<div class="section">
		<a href="/RawNOLAs">Back to NOLA Records</a>
		<div class="ActionBox">
			<form>
				<div class="title-container">
					<h3 class="title is-2">Edit NOLA Record</h3>
					{#if NOLA.NOLA_ID.length}
						<button class="button is-danger" type="button" on:click={confirmDelete}>Delete</button>
					{/if}
				</div>

				<!-- Read-Only NOLA_ID -->
				<div class="control">
					<div class="field">
						<label class="label" for="NOLA_ID">NOLA ID</label>
						<input class="input" type="text" id="NOLA_ID" bind:value={NOLA.NOLA_ID} readonly />
					</div>
				</div>

				<br />

				<!-- First Party -->
				<div class="control">
					<label class="label" for="FirstParty">First Party</label>
					<div class="field">
						<input class="input" type="text" id="FirstParty" bind:value={NOLA.FirstParty}  />
					</div>
				</div>

				<!-- Location First Party -->
				<div class="control">
					<label class="label" for="LocationFirstParty">Location First Party</label>
					<div class="field">
						<input class="input" type="text" id="LocationFirstParty" bind:value={NOLA.LocationFirstParty} />
					</div>
				</div>

				<!-- Second Party -->
				<div class="control">
					<label class="label" for="SecondParty">Second Party</label>
					<div class="field">
						<input class="input" type="text" id="SecondParty" bind:value={NOLA.SecondParty}  />
					</div>
				</div>

				<!-- Location Second Party -->
				<div class="control">
					<label class="label" for="LocationSecondParty">Location Second Party</label>
					<div class="field">
						<input class="input" type="text" id="LocationSecondParty" bind:value={NOLA.LocationSecondParty} />
					</div>
				</div>

				<!-- Type of Transaction -->
				<div class="control">
					<label class="label" for="TypeOfTransaction">Type of Transaction</label>
					<div class="field">
						<input class="input" type="text" id="TypeOfTransaction" bind:value={NOLA.TypeOfTransaction}  />
					</div>
				</div>

				<!-- Date of Transaction -->
				<div class="control">
					<label class="label" for="DateOfTransaction">Date of Transaction</label>
					<div class="field">
						<input class="input" type="date" id="DateOfTransaction" bind:value={NOLA.DateOfTransaction} />
					</div>
				</div>

				<!-- Act -->
				<div class="control">
					<label class="label" for="Act">Act</label>
					<div class="field">
						<input class="input" type="text" id="Act" bind:value={NOLA.Act} />
					</div>
				</div>

				<!-- Page -->
				<div class="control">
					<label class="label" for="Page">Page</label>
					<div class="field">
						<input class="input" type="text" id="Page" bind:value={NOLA.Page} />
					</div>
				</div>

				<!-- Notary Public -->
				<div class="control">
					<label class="label" for="NotaryPublic">Notary Public</label>
					<div class="field">
						<input class="input" type="text" id="NotaryPublic" bind:value={NOLA.NotaryPublic} />
					</div>
				</div>

				<!-- Volume -->
				<div class="control">
					<label class="label" for="Volume">Volume</label>
					<div class="field">
						<input class="input" type="text" id="Volume" bind:value={NOLA.Volume} />
					</div>
				</div>

				<!-- Name of Transcriber -->
				<div class="control">
					<label class="label" for="NameOfTranscriber">Name of Transcriber</label>
					<div class="field">
						<input class="input" type="text" id="NameOfTranscriber" bind:value={NOLA.NameOfTranscriber} />
					</div>
				</div>

				<!-- Reference URL -->
				<div class="control">
					<label class="label" for="ReferenceURL">Reference URL</label>
					<div class="field">
						<input class="input" type="url" id="ReferenceURL" bind:value={NOLA.ReferenceURL} />
					</div>
				</div>

				<div class="field">
					<div class="control">
						<button class="button is-primary" type="button" on:click={() => handleSaveNOLA(Session.SessionId, NOLA, true)}>Save</button>

					</div>
				</div>
			</form>
		</div>
	</div>
{/if}
