<style>
	.buttons-container {
	display: flex;
	justify-content: space-between; /* Pushes Save left, Delete right */
	align-items: center;
	width: 100%; /* Ensures full width */
}

.delete-button {
	margin-left: auto; /* Pushes Delete to the right */
}

</style>
<script>
	import { onMount } from 'svelte';
	import { Session } from '../Session.js';
	import { handleGetHuman } from './handleGetHuman.js';
	import { saveHuman } from './handleSaveHuman.js';
	import { handleDelete } from './handleDelete.js'; // Import delete function

	let Human = {
		FirstName: '',
		MiddleName: '',
		LastName: '',
		BirthDate: '',
		BirthDateAccuracy: 'd',
		RacialDescriptor: '',
		Sex: '',
		Height_cm: '',
		Roles: ''
	};

	let isLoading = true;
	let HumanId = null;

	// Get HumanId from URL
	function getHumanIdFromURL() {
		const params = new URLSearchParams(window.location.search);
		return params.get("HumanId") || null;
	}

	onMount(async () => {
		await Session.handleSession();
		HumanId = getHumanIdFromURL();

		if (HumanId) {
			const data = await handleGetHuman(Session.SessionId, HumanId);
			if (data) {
				Human = { ...data };
				Human.Roles = data.Roles ? data.Roles.join(', ') : '';
			}
		}

		// Convert stored cm to inches for display
		if (Human.Height_cm) {
			Human.Height_in = (Human.Height_cm / 2.54).toFixed(2); // Rounded to 2 decimal places
		} else {
			Human.Height_in = '';
		}

		isLoading = false;
	});

	async function submitHuman() {
		const success = await saveHuman(Session.SessionId, HumanId, Human);
		if (success) {
			window.location.href = '/Humans'; // Redirect after saving
		} else {
			alert("Failed to save human.");
		}
	}

	async function deleteHuman() {
		if (confirm("Are you sure you want to delete this human? This action cannot be undone.")) {
			await handleDelete(Session.SessionId, HumanId);
		}
	}
</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner"></div>
	</div>
{:else}
	<div class="section">
		<a href="/Humans">Back to List</a>
		<h3 class="title is-2">{HumanId ? 'Edit' : 'Add'} Human</h3>
		
		<form on:submit|preventDefault={submitHuman}>
			<div class="field">
				<label for="first-name">First Name:</label>
				<input id="first-name" class="input" type="text" bind:value={Human.FirstName} />
			</div>

			<div class="field">
				<label for="middle-name">Middle Name:</label>
				<input id="middle-name" class="input" type="text" bind:value={Human.MiddleName} />
			</div>

			<div class="field">
				<label for="last-name">Last Name:</label>
				<input id="last-name" class="input" type="text" bind:value={Human.LastName} />
			</div>

			<div class="field">
				<label for="birth-date">Birth Date:</label>
				<input id="birth-date" class="input" type="date" bind:value={Human.BirthDate} />
			</div>

			<div class="field">
				<label for="birth-accuracy">Birth Date Accuracy:</label>
				<select id="birth-accuracy" class="input" bind:value={Human.BirthDateAccuracy}>
					<option value="d">Day</option>
					<option value="m">Month</option>
					<option value="y">Year</option>
				</select>
			</div>

			<div class="field">
				<label for="racial-descriptor">Racial Descriptor:</label>
				<input id="racial-descriptor" class="input" type="text" bind:value={Human.RacialDescriptor} />
			</div>

			<div class="field">
				<label for="sex">Sex:</label>
				<input id="sex" class="input" type="text" bind:value={Human.Sex} />
			</div>

			<div class="field">
				<label for="height-inches">Height (inches):</label>
				<input id="height-inches" class="input" type="number" step="0.01" bind:value={Human.Height_in} min="0" />
			</div>

			<div class="field">
				<label for="roles">Roles (comma-separated):</label>
				<input id="roles" class="input" type="text" bind:value={Human.Roles} placeholder="Role1, Role2, ..." />
			</div>

			<div class="buttons-container">
				<button class="button is-primary" type="submit">Save</button>
				{#if HumanId} 
					<button class="button is-danger delete-button" type="button" on:click={deleteHuman}>Delete</button>
				{/if}
			</div>
		</form>
	</div>
{/if}
