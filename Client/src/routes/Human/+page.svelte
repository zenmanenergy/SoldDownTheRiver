<script>
	import { onMount } from 'svelte';
	import { Session } from '../Session.js';
	import { handleGetHumanById, handleSaveHuman } from './handleHumans.js';

	let Human = {
		FirstName: '',
		MiddleName: '',
		LastName: '',
		BirthDate: '',
		BirthDateAccuracy: 'd',
		RacialDescriptor: '',
		Sex: '',
		Height_in: '',
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
			const data = await handleGetHumanById(Session.SessionId, HumanId);
			if (data) {
				Human = { ...data };
				Human.Roles = data.Roles ? data.Roles.join(', ') : '';
			}
		}

		isLoading = false;
	});

	async function saveHuman() {
		// Convert Roles to an array
		Human.Roles = Human.Roles.split(',').map(role => role.trim());

		const success = await handleSaveHuman(Session.SessionId, HumanId, Human);

		if (success) {
			window.location.href = '/HumansList'; // Redirect after saving
		} else {
			alert("Failed to save human.");
		}
	}
</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner"></div>
	</div>
{:else}
	<div class="section">
		<a href="/HumansList">Back to List</a>
		<h3 class="title is-2">{HumanId ? 'Edit' : 'Add'} Human</h3>
		
		<form on:submit|preventDefault={saveHuman}>
			<div class="field">
				<label>First Name:</label>
				<input class="input" type="text" bind:value={Human.FirstName} required />
			</div>

			<div class="field">
				<label>Middle Name:</label>
				<input class="input" type="text" bind:value={Human.MiddleName} />
			</div>

			<div class="field">
				<label>Last Name:</label>
				<input class="input" type="text" bind:value={Human.LastName} required />
			</div>

			<div class="field">
				<label>Birth Date:</label>
				<input class="input" type="date" bind:value={Human.BirthDate} />
			</div>

			<div class="field">
				<label>Birth Date Accuracy:</label>
				<select class="input" bind:value={Human.BirthDateAccuracy}>
					<option value="d">Day</option>
					<option value="m">Month</option>
					<option value="y">Year</option>
				</select>
			</div>

			<div class="field">
				<label>Racial Descriptor:</label>
				<input class="input" type="text" bind:value={Human.RacialDescriptor} />
			</div>

			<div class="field">
				<label>Sex:</label>
				<input class="input" type="text" bind:value={Human.Sex} />
			</div>

			<div class="field">
				<label>Height (inches):</label>
				<input class="input" type="number" bind:value={Human.Height_in} min="0" />
			</div>

			<div class="field">
				<label>Roles (comma-separated):</label>
				<input class="input" type="text" bind:value={Human.Roles} placeholder="Role1, Role2, ..." />
			</div>

			<div class="buttons">
				<button class="button is-primary" type="submit">Save</button>
			</div>
		</form>
	</div>
{/if}
