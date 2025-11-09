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

	.pagination {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 1rem;
		margin-top: 1rem;
	}
</style>

<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleGetShips } from './handleGetShips.js';
	import { Session } from "../../Session.js";

	let Ships = [];
	let filteredShips = [];
	let isLoading = true;
	let searchQuery = '';
	let filterOption = 'all';

	let currentPage = 1;
	let itemsPerPage = 50;
	let totalPages = 1;

	let sortColumn = 'ShipName';
	let sortAscending = true;

	onMount(async () => {
		await Session.handleSession();
		await handleGetShips(Session.SessionId, setShips);
		isLoading = false;
	});

	function setShips(data) {
		Ships = data;
	}

	$: {
		filteredShips = Ships.filter(ship => {
			// Filter by approval status
			if (filterOption === 'unapproved' && ship.isApproved !== 0) {
				return false;
			}
			
			const search = searchQuery.toLowerCase();
			const values = [
				ship.ShipName,
				ship.ShipType,
				ship.CaptainName
			];
			return values.some(value => value && value.toLowerCase().includes(search));
		});

		// Sort the filtered ships
		filteredShips.sort((a, b) => {
			let valueA = a[sortColumn] ?? '';
			let valueB = b[sortColumn] ?? '';

			// Convert to lowercase for case-insensitive sorting
			if (typeof valueA === 'string') valueA = valueA.toLowerCase();
			if (typeof valueB === 'string') valueB = valueB.toLowerCase();

			if (valueA < valueB) return sortAscending ? -1 : 1;
			if (valueA > valueB) return sortAscending ? 1 : -1;
			return 0;
		});

		currentPage = 1;
		totalPages = Math.max(1, Math.ceil(filteredShips.length / itemsPerPage));
	}

	$: displayedShips = filteredShips.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

	function toggleSort(column) {
		if (sortColumn === column) {
			sortAscending = !sortAscending;
		} else {
			sortColumn = column;
			sortAscending = true;
		}
	}

	function addShip() {
		window.location.href = '/Admin/Ship?ShipId=';
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
				<h3 class="title is-2">List of Ships</h3>
				<button class="button is-primary" on:click={addShip}>Add Ship</button>
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
				Showing {filteredShips.length} record{filteredShips.length !== 1 ? 's' : ''}
			</div>
			
			<table class="table is-striped is-hoverable is-fullwidth">
				<thead>
					<tr>
						<th on:click={() => toggleSort('ShipName')}>Ship Name</th>
						<th on:click={() => toggleSort('ShipType')}>Ship Type</th>
					</tr>
				</thead>
				<tbody>
					{#each displayedShips as ship}
						<tr on:click={() => window.location.href = `/Admin/Ship?ShipId=${ship.ShipId}`}>
							<td>{ship.ShipName || ''}</td>
							<td>{ship.ShipType || ''}</td>
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
