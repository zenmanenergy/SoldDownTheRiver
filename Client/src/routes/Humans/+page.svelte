<style>
	@import '/static/FormPages.css';
</style>

<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { Session } from "../Session.js";
	import { handleGetHumans } from './handleGetHumans.js';

	let Humans = [];
	let filteredHumans = [];
	let isLoading = true;
	let searchQuery = '';

	let currentPage = 1;
	let itemsPerPage = 50;
	let totalPages = 1;

	// Extract search parameter from the URL
	function getSearchQueryFromURL() {
		const params = new URLSearchParams(window.location.search);
		return params.get("search") || ''; // Default to empty string if missing
	}


	onMount(async () => {
		// Get search query from URL on page load
		searchQuery = getSearchQueryFromURL();

		await Session.handleSession();
		await handleGetHumans(Session.SessionId, setHumans);

		isLoading = false;
	});


	function setHumans(data) {
		Humans = data;
	}

	$: {
		filteredHumans = Humans.filter(human => {
			const search = searchQuery.toLowerCase();

			function formatBirthDate(date, accuracy) {
				if (!date) return '';
				const formattedDate = moment.utc(date);
				switch (accuracy?.toLowerCase()) {
					case 'd': return formattedDate.format('YYYY-MM-DD');
					case 'm': return formattedDate.format('YYYY-MM');
					case 'y': return formattedDate.format('YYYY');
					default: return formattedDate.format('YYYY-MM-DD');
				}
			}

			const values = [
				human.FirstName,
				human.MiddleName,
				human.LastName,
				formatBirthDate(human.BirthDate, human.BirthDateAccuracy),
				human.RacialDescriptor,
				human.Sex,
				human.Height_in ? human.Height_in.toString() : '',
				human.Roles ? human.Roles.join(', ') : ''
			];

			return values.some(value => value && value.toLowerCase().includes(search));
		});

		currentPage = 1; // Reset to first page when filtering
		totalPages = Math.max(1, Math.ceil(filteredHumans.length / itemsPerPage));
	}

	$: displayedHumans = filteredHumans.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

	function formatBirthDate(date, accuracy) {
		if (!date) return '';
		const formattedDate = moment.utc(date);
		switch (accuracy?.toLowerCase()) {
			case 'd': return formattedDate.format('YYYY-MM-DD'); // Full date
			case 'm': return formattedDate.format('YYYY-MM');    // Year & Month
			case 'y': return formattedDate.format('YYYY');       // Only Year
			default: return formattedDate.format('YYYY-MM-DD');  // Default to full date
		}
	}



	$: totalPages = Math.ceil(filteredHumans.length / itemsPerPage);

	function addHuman() {
		window.location.href = '/Human?HumanId=';
	}
</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner"></div>
	</div>
{:else}
	<div class="section">
		<a href="/AdminMenu">Back to Menu</a>
		<div class="ActionBox">
			<div class="title-container">
				<h3 class="title is-2">List of Humans</h3>
				<button class="button is-primary" on:click={addHuman}>Add Human</button>
			</div>
			<form>
				<div class="field">
					<div class="control">
						<input class="input" type="text" bind:value={searchQuery} placeholder="Search by name" />
					</div>
				</div>
			</form>
			<table class="ClickableTable">
				<thead>
					<tr>
						<th>First Name</th>
						<th>Middle Name</th>
						<th>Last Name</th>
						<th>Birth Date</th>
						<th>Racial Descriptor</th>
						<th>Sex</th>
						<th>Height (inches)</th>
						<th>Roles</th> <!-- New Column -->
					</tr>
				</thead>
				<tbody>
					{#each displayedHumans as human}
						<tr on:click={() => window.location.href = `/Human?HumanId=${human.HumanId}`} style="cursor: pointer;">

							<td>{human.FirstName}</td>
							<td>{human.MiddleName || ''}</td>
							<td>{human.LastName}</td>
							<td>{formatBirthDate(human.BirthDate, human.BirthDateAccuracy)}</td>
							<td>{human.RacialDescriptor || ''}</td>
							<td>{human.Sex || ''}</td>
							<td>{human.Height_in ? `${human.Height_cm*2.54} in` : ''}</td>
							<td>{human.Roles.length > 0 ? human.Roles.join(', ') : 'No Roles'}</td> <!-- New Column -->
						</tr>
					{/each}
				</tbody>
			</table>
			
			<div class="pagination">
				<button on:click={() => currentPage = Math.max(currentPage - 1, 1)} disabled={currentPage === 1}>
					Previous
				</button>
				<span>{currentPage} / {totalPages}</span>
				<button on:click={() => currentPage = Math.min(currentPage + 1, totalPages)} disabled={currentPage === totalPages}>
					Next
				</button>
			</div>
		</div>
	</div>
{/if}
