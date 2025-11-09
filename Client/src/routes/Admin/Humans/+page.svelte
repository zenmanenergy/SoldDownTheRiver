<style>
	@import '/static/FormPages.css';

	.field.is-grouped {
		display: flex;
		align-items: flex-end;
		gap: 0.75rem;
		margin-bottom: 0.75rem;
	}

	.field.is-grouped .control.is-expanded {
		flex: 1;
	}

	.field.is-grouped .control {
		margin-bottom: 0;
	}

	.field.is-grouped .input,
	.field.is-grouped .select select {
		height: 2.5rem;
		box-sizing: border-box;
	}

	.field.is-grouped .select {
		height: 2.5rem;
	}
</style>
<script>
// Helper to clip long text and add ellipsis
function clipText(text, maxLength = 40) {
	if (!text) return '';
	return text.length > maxLength ? text.slice(0, maxLength) + '...' : text;
}
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { Session } from "../../Session.js";
	import { handleGetHumans } from './handleGetHumans.js';

	let Humans = [];
	let filteredHumans = [];
	let isLoading = true;
	let searchQuery = '';
	let filterOption = 'all'; // 'all' or 'unapproved'

	let currentPage = 1;
	let itemsPerPage = 100;
	let totalPages = 1;

	let sortColumn = 'LastName';
	let sortAscending = true;

	let relationshipTree = [];

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

	function isAlreadyInRelationship(humanId) {
		return relationshipTree.includes(humanId);
	}

	function insertRelationship(humanId) {
		if (!isAlreadyInRelationship(humanId)) {
			relationshipTree.push(humanId);
			// ...code to persist the new relationship...
		} else {
			alert('This human is already in the relationship tree.');
		}
	}

	$: {
		filteredHumans = Humans.filter(human => {
			// Apply approval status filter
			if (filterOption === 'unapproved') {
				// Only show records where isApproved is exactly 0
				if (human.isApproved !== 0) {
					return false;
				}
			}
			// filterOption === 'all' shows everything regardless of isApproved value
			
			const search = searchQuery.toLowerCase();
			const values = [
				human.FirstName,
				human.MiddleName,
				human.LastName,
				formatBirthDate(human.BirthDate, human.BirthDateAccuracy),
				human.RacialDescriptor,
				human.Sex,
				human.Roles ? human.Roles.join(', ') : '',
				human.HumanId, // Include HumanId in the search,
				human.AlsoKnownAs ? human.AlsoKnownAs.join(', ') : ''
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
		window.location.href = '/Admin/Human?HumanId=';
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
				<h3 class="title is-2">List of Humans</h3>
				<button class="button is-primary" on:click={addHuman}>Add Human</button>
			</div>
			<form>
				<div class="field is-grouped">
					<div class="control is-expanded">
						<input class="input" type="text" bind:value={searchQuery} placeholder="Search by name" />
					</div>
					<div class="control">
						<div class="select">
							<select bind:value={filterOption}>
								<option value="all">Show all</option>
								<option value="unapproved">Unapproved</option>
							</select>
						</div>
					</div>
				</div>
			</form>
			
			<!-- Record count display -->
			<div class="record-count" style="margin: 1rem 0; font-weight: bold; color: #363636;">
				Showing {filteredHumans.length} record{filteredHumans.length !== 1 ? 's' : ''}
			</div>
			
			<table class="table is-striped is-hoverable is-fullwidth">
				<thead>
					<tr>
						<th on:click={() => toggleSort('FirstName')}>First Name</th>
						<th on:click={() => toggleSort('LastName')}>Last Name</th>
						<th on:click={() => toggleSort('BirthDate')}>Birth Date</th>
						<th on:click={() => toggleSort('RacialDescriptor')}>Racial Descriptor</th>
						<th on:click={() => toggleSort('Sex')}>Sex</th>
						<th on:click={() => toggleSort('Roles')}>Roles</th>
					</tr>
				</thead>
				<tbody>
					{#each displayedHumans as human}
						<tr on:click={() => window.open(`/Admin/Human?HumanId=${human.HumanId}`, '_blank')}>
							<td>{clipText((human.FirstName || '') + (human.MiddleName ? ' ' + human.MiddleName : ''))}</td>
							<td>{clipText(human.LastName || '')}</td>
							<td>{clipText(formatBirthDate(human.BirthDate, human.BirthDateAccuracy) || '')}</td>
							<td>{clipText(human.RacialDescriptor || '')}</td>
							<td>{clipText(human.Sex || '')}</td>
							<td>{clipText(human.Roles && human.Roles.length > 0 ? human.Roles.join(', ') : '')}</td>
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
