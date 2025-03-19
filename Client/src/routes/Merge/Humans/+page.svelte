<style>
	@import '/static/FormPages.css';
	.table tbody tr:hover {
		background-color: #f0f0f0;
		cursor: pointer;
	}
</style>
<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { Session } from "../../Session.js";
	import { handleGetHumans } from './handleGetHumans.js';

	let Humans = [];
	let filteredHumans = [];
	let isLoading = true;
	let searchQuery = '';

	let currentPage = 1;
	let itemsPerPage = 50;
	let totalPages = 1;

	let sortColumn = 'LastName';
	let sortAscending = true;

	let selectedHumans = [];

	function getSearchQueryFromURL() {
		const params = new URLSearchParams(window.location.search);
		return params.get("search") || ''; // Default to empty string if missing
	}

	onMount(async () => {
		searchQuery = getSearchQueryFromURL();
		await Session.handleSession();
		await handleGetHumans(Session.SessionId, setHumans);
		isLoading = false;
	});

	function setHumans(data) {
		Humans = data;
	}

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

	$: {
		filteredHumans = Humans.filter(human => {
			const search = searchQuery.toLowerCase();
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

		// Sort the filtered humans
		filteredHumans.sort((a, b) => {
			let valueA = a[sortColumn] ?? '';
			let valueB = b[sortColumn] ?? '';

			// Handle birth date sorting separately
			if (sortColumn === 'BirthDate') {
				valueA = a.BirthDate ? new Date(a.BirthDate) : new Date(0);
				valueB = b.BirthDate ? new Date(b.BirthDate) : new Date(0);
			}

			// Convert numeric values
			if (sortColumn === 'Height_in') {
				valueA = parseFloat(a.Height_in) || 0;
				valueB = parseFloat(b.Height_in) || 0;
			}

			// Convert to lowercase for case-insensitive sorting
			if (typeof valueA === 'string') valueA = valueA.toLowerCase();
			if (typeof valueB === 'string') valueB = valueB.toLowerCase();

			if (valueA < valueB) return sortAscending ? -1 : 1;
			if (valueA > valueB) return sortAscending ? 1 : -1;
			return 0;
		});

		currentPage = 1; 
		totalPages = Math.max(1, Math.ceil(filteredHumans.length / itemsPerPage));
	}

	$: displayedHumans = filteredHumans.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

	function toggleSort(column) {
		if (sortColumn === column) {
			sortAscending = !sortAscending;
		} else {
			sortColumn = column;
			sortAscending = true;
		}
	}

	function addHuman() {
		window.location.href = '/Human?HumanId=';
	}

	function selectHuman(human) {
		if (!selectedHumans.find(h => h.HumanId === human.HumanId)) {
			selectedHumans = [...selectedHumans, human];
		}
	}

	function removeSelectedHuman(humanId) {
		selectedHumans = selectedHumans.filter(h => h.HumanId !== humanId);
	}

	function openHumanInNewTab(humanId) {
		if (selectedHumans.length === 2) {
			const [human1, human2] = selectedHumans;
			const win1 = window.open(`/Human?HumanId=${human1.HumanId}&mergeHumanId=${human2.HumanId}`, '_blank1');
			setTimeout(() => {
				const win2 = window.open(`/Human?HumanId=${human2.HumanId}&mergeHumanId=${human1.HumanId}`, '_blank2');
				if (!win2) {
					alert("Please allow pop-ups for this website to compare humans.");
				}
			}, 500);
			if (!win1) {
				alert("Please allow pop-ups for this website to compare humans.");
			}
		} else {
			alert("Please select exactly 2 humans to compare.");
		}
	}
</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner"></div>
	</div>
{:else}
	<div class="section">
		
		<div class="ActionBox">

			<h3 class="title is-3">Selected Humans for merging </h3>
			{#if selectedHumans.length > 0}
				<table class="table is-fullwidth is-striped">
					<thead>
						<tr>
							<th>First Name</th>
							<th>Last Name</th>
							<th>Actions</th>
						</tr>
					</thead>
					<tbody>
						{#each selectedHumans as human}
							<tr on:click={() => openHumanInNewTab(human.HumanId)} style="cursor: pointer;">
								<td>{human.FirstName}</td>
								<td>{human.LastName}</td>
								<td>
									<button class="button is-danger" on:click={() => removeSelectedHuman(human.HumanId)}>Remove</button>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			{:else}
				<div class="notification is-warning">Select 2 Humans below</div>
			{/if}
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
						<th on:click={() => toggleSort('FirstName')} style="cursor: pointer;">First Name</th>
						<th on:click={() => toggleSort('MiddleName')} style="cursor: pointer;">Middle Name</th>
						<th on:click={() => toggleSort('LastName')} style="cursor: pointer;">Last Name</th>
						<th on:click={() => toggleSort('BirthDate')} style="cursor: pointer;">Birth Date</th>
						<th on:click={() => toggleSort('RacialDescriptor')} style="cursor: pointer;">Racial Descriptor</th>
						<th on:click={() => toggleSort('Sex')} style="cursor: pointer;">Sex</th>
						<th on:click={() => toggleSort('Height_in')} style="cursor: pointer;">Height (inches)</th>
						<th on:click={() => toggleSort('Roles')} style="cursor: pointer;">Roles</th>
					</tr>
				</thead>
				<tbody>
					{#each displayedHumans as human}
						<tr on:click={() => selectHuman(human)} style="cursor: pointer;">
							<td>{human.FirstName || ''}</td>
							<td>{human.MiddleName || ''}</td>
							<td>{human.LastName || ''}</td>
							<td>{formatBirthDate(human.BirthDate, human.BirthDateAccuracy)}</td>
							<td>{human.RacialDescriptor || ''}</td>
							<td>{human.Sex || ''}</td>
							<td>{human.Height_in ? `${human.Height_in} in` : ''}</td>
							<td>{human.Roles.length > 0 ? human.Roles.join(', ') : 'No Roles'}</td>
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
