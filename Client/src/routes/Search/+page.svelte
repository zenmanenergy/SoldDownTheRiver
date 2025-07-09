<style>
	@import '/static/FormPages.css';
</style>
<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { Session } from "../../Session.js";
	import { handleGetHumans } from '../Humans/handleGetHumans.js';

	let searchType = 'People';
	let searchQuery = '';
	let Humans = [];
	let filteredHumans = [];
	let isLoading = true;

	let currentPage = 1;
	let itemsPerPage = 50;
	let totalPages = 1;

	let sortColumn = 'LastName';
	let sortAscending = true;

	const searchTypes = ['People', 'Transactions', 'Ships'];

	onMount(async () => {
		await Session.handleSession();
		if (searchType === 'People') {
			await handleGetHumans(Session.SessionId, setHumans);
		}
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

	// Reactive statement - exactly like Humans page
	$: {
		filteredHumans = Humans.filter(human => {
			const search = searchQuery.toLowerCase();
			const searchWords = search.trim().split(/\s+/).filter(word => word.length > 0);
			
			// If no search words, show all humans
			if (searchWords.length === 0) {
				return true;
			}
			
			const values = [
				human.FirstName,
				human.MiddleName,
				human.LastName,
				formatBirthDate(human.BirthDate, human.BirthDateAccuracy),
				human.RacialDescriptor,
				human.Sex,
				human.Height_in ? human.Height_in.toString() : '',
				human.Roles ? human.Roles.join(', ') : '',
				human.HumanId,
				human.AlsoKnownAs ? human.AlsoKnownAs.join(', ') : ''
			];
			
			// Combine all searchable values into one string
			const searchableText = values.join(' ').toLowerCase();
			
			// Check that ALL search words are found in the searchable text
			return searchWords.every(word => searchableText.includes(word));
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

	// Watch for searchType changes to load appropriate data
	$: {
		if (searchType === 'People' && Humans.length === 0 && !isLoading) {
			isLoading = true;
			handleGetHumans(Session.SessionId, setHumans).then(() => {
				isLoading = false;
			});
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
			<div class="title-container">
				<h3 class="title is-2">Search</h3>
			</div>
			
			<form>
				<div class="field">
					<label class="label">Search Type:</label>
					<div class="control">
						<div class="select">
							<select bind:value={searchType}>
								{#each searchTypes as type}
									<option value={type}>{type}</option>
								{/each}
							</select>
						</div>
					</div>
				</div>
				<div class="field">
					<div class="control">
						<input class="input" type="text" bind:value={searchQuery} placeholder="Search by name" />
					</div>
				</div>
			</form>
			
			{#if searchType === 'People'}
				<table class="table is-striped is-hoverable is-fullwidth">
					<thead>
						<tr>
							<th on:click={() => toggleSort('FirstName')}>First Name</th>
							<th on:click={() => toggleSort('LastName')}>Last Name</th>
							<th on:click={() => toggleSort('BirthDate')}>Birth Date</th>
							<th on:click={() => toggleSort('RacialDescriptor')}>Racial Descriptor</th>
							<th on:click={() => toggleSort('Sex')}>Sex</th>
							<th on:click={() => toggleSort('Height_in')}>Height (inches)</th>
							<th on:click={() => toggleSort('Roles')}>Roles</th>
						</tr>
					</thead>
					<tbody>
						{#each displayedHumans as human}
							<tr on:click={() => window.location.href = `/Admin/Reports/Human?HumanId=${human.HumanId}`}>
								<td>{human.FirstName || ''}{' ' & human.MiddleName || ''}</td>
								<td>{human.LastName || ''}</td>
								<td>{formatBirthDate(human.BirthDate, human.BirthDateAccuracy) || ''}</td>
								<td>{human.RacialDescriptor || ''}</td>
								<td>{human.Sex || ''}</td>
								<td>{human.Height_in ? `${human.Height_in} in` : ''}</td>
								<td>{human.Roles.length > 0 ? human.Roles.join(', ') : ''}</td>
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
			{:else}
				<p>Search for {searchType} is not yet implemented.</p>
			{/if}
		</div>
	</div>
{/if}