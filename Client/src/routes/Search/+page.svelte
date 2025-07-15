<style>
	@import '/static/FormPages.css';
</style>
<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleSearchHumans } from './handleSearchHumans.js';
	import { handleSearchShips } from './handleSearchShips.js';
	import { handleSearchTransactions } from './handleSearchTransactions.js';

	let searchType = 'People';
	let searchQuery = '';
	let Humans = [];
	let Ships = [];
	let Transactions = [];
	let filteredHumans = [];
	let filteredShips = [];
	let filteredTransactions = [];
	let isLoading = true;

	let currentPage = 1;
	let itemsPerPage = 50;
	let totalPages = 1;

	let sortColumn = 'LastName';
	let sortAscending = true;

	const searchTypes = ['People', 'Transactions', 'Ships'];

	onMount(async () => {
		await handleSearchHumans(setHumans);
		await handleSearchShips(setShips);
		await handleSearchTransactions(setTransactions);
		isLoading = false;
	});

	function setHumans(data) {
		Humans = data;
	}
	function setShips(data) {
		Ships = data;
	}
	function setTransactions(data) {
		Transactions = data;
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

	function formatTransactionDate(date, accuracy) {
		if (!date) return '';
		const formattedDate = moment.utc(date);
		switch (accuracy?.toLowerCase()) {
			case 'd': return formattedDate.format('YYYY-MM-DD');
			case 'm': return formattedDate.format('YYYY-MM');
			case 'y': return formattedDate.format('YYYY');
			default: return formattedDate.format('YYYY-MM-DD');
		}
	}

	// Reactive statement for filtering humans
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

	// Reactive statement for filtering ships
	$: {
		filteredShips = Ships.filter(ship => {
			const search = searchQuery.toLowerCase();
			const searchWords = search.trim().split(/\s+/).filter(word => word.length > 0);
			
			// If no search words, show all ships
			if (searchWords.length === 0) {
				return true;
			}
			
			const values = [
				ship.ShipName,
				ship.ShipType,
				ship.Flag,
				ship.Captain,
				ship.Owner,
				ship.Builder,
				ship.BuildYear ? ship.BuildYear.toString() : '',
				ship.Tonnage ? ship.Tonnage.toString() : '',
				ship.Description
			];
			
			// Combine all searchable values into one string
			const searchableText = values.join(' ').toLowerCase();
			
			// Check that ALL search words are found in the searchable text
			return searchWords.every(word => searchableText.includes(word));
		});

		// Sort the filtered ships
		filteredShips.sort((a, b) => {
			let valueA = a[sortColumn] ?? '';
			let valueB = b[sortColumn] ?? '';

			// Convert numeric values
			if (sortColumn === 'BuildYear' || sortColumn === 'Tonnage') {
				valueA = parseFloat(a[sortColumn]) || 0;
				valueB = parseFloat(b[sortColumn]) || 0;
			}

			// Convert to lowercase for case-insensitive sorting
			if (typeof valueA === 'string') valueA = valueA.toLowerCase();
			if (typeof valueB === 'string') valueB = valueB.toLowerCase();

			if (valueA < valueB) return sortAscending ? -1 : 1;
			if (valueA > valueB) return sortAscending ? 1 : -1;
			return 0;
		});

		if (searchType === 'Ships') {
			totalPages = Math.max(1, Math.ceil(filteredShips.length / itemsPerPage));
		}
	}

	// Reactive statement for filtering transactions
	$: {
		filteredTransactions = Transactions.filter(transaction => {
			const search = searchQuery.toLowerCase();
			const searchWords = search.trim().split(/\s+/).filter(word => word.length > 0);
			
			// If no search words, show all transactions
			if (searchWords.length === 0) {
				return true;
			}
			
			const values = [
				transaction.TransactionType,
				transaction.date_circa,
				transaction.TotalPrice ? transaction.TotalPrice.toString() : '',
				transaction.Act,
				transaction.Page,
				transaction.Volume,
				transaction.LocationAddress,
				transaction.LocationCity,
				transaction.LocationCounty,
				transaction.LocationStateAbbr,
				transaction.Buyers,
				transaction.Sellers,
				transaction.Notary,
				transaction.TransactionId,
				transaction.URL
			];
			
			// Combine all searchable values into one string
			const searchableText = values.join(' ').toLowerCase();
			
			// Check that ALL search words are found in the searchable text
			return searchWords.every(word => searchableText.includes(word));
		});

		// Sort the filtered transactions
		filteredTransactions.sort((a, b) => {
			let valueA = a[sortColumn] ?? '';
			let valueB = b[sortColumn] ?? '';

			// Handle date sorting separately
			if (sortColumn === 'date_circa') {
				valueA = a.date_circa ? new Date(a.date_circa) : new Date(0);
				valueB = b.date_circa ? new Date(b.date_circa) : new Date(0);
			}

			// Convert numeric values
			if (sortColumn === 'TotalPrice') {
				valueA = parseFloat(a.TotalPrice) || 0;
				valueB = parseFloat(b.TotalPrice) || 0;
			}

			// Convert to lowercase for case-insensitive sorting
			if (typeof valueA === 'string') valueA = valueA.toLowerCase();
			if (typeof valueB === 'string') valueB = valueB.toLowerCase();

			if (valueA < valueB) return sortAscending ? -1 : 1;
			if (valueA > valueB) return sortAscending ? 1 : -1;
			return 0;
		});

		if (searchType === 'Transactions') {
			totalPages = Math.max(1, Math.ceil(filteredTransactions.length / itemsPerPage));
		}
	}

	$: displayedHumans = filteredHumans.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);
	$: displayedShips = filteredShips.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);
	$: displayedTransactions = filteredTransactions.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

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
			handleSearchHumans(setHumans).then(() => {
				isLoading = false;
			});
		}
	}

	// Clear search query when search type changes
	$: {
		if (searchType) {
			searchQuery = '';
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
					<label class="label" for="searchType">Search Type:</label>
					<div class="control">
						<div class="select">
							<select id="searchType" bind:value={searchType}>
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
							<tr on:click={() => window.location.href = `/Reports/Human?HumanId=${human.HumanId}`}>
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
			{:else if searchType === 'Ships'}
				<table class="table is-striped is-hoverable is-fullwidth">
					<thead>
						<tr>
							<th on:click={() => toggleSort('ShipName')}>Ship Name</th>
							<th on:click={() => toggleSort('ShipType')}>Ship Type</th>
							<th on:click={() => toggleSort('Flag')}>Flag</th>
							<th on:click={() => toggleSort('Captain')}>Captain</th>
							<th on:click={() => toggleSort('Owner')}>Owner</th>
							<th on:click={() => toggleSort('BuildYear')}>Build Year</th>
							<th on:click={() => toggleSort('Tonnage')}>Tonnage</th>
						</tr>
					</thead>
					<tbody>
						{#each displayedShips as ship}
							<tr on:click={() => window.location.href = `/Reports/Ship?ShipId=${ship.ShipId}`}>
								<td>{ship.ShipName || ''}</td>
								<td>{ship.ShipType || ''}</td>
								<td>{ship.Flag || ''}</td>
								<td>{ship.Captain || ''}</td>
								<td>{ship.Owner || ''}</td>
								<td>{ship.BuildYear || ''}</td>
								<td>{ship.Tonnage || ''}</td>
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
			{:else if searchType === 'Transactions'}
				<table class="table is-striped is-hoverable is-fullwidth">
					<thead>
						<tr>
							<th on:click={() => toggleSort('TransactionType')}>Type</th>
							<th on:click={() => toggleSort('date_circa')}>Date</th>
							<th on:click={() => toggleSort('TotalPrice')}>Total Price</th>
							<th on:click={() => toggleSort('LocationCity')}>City</th>
							<th on:click={() => toggleSort('LocationStateAbbr')}>State</th>
							<th on:click={() => toggleSort('Buyers')}>Buyers</th>
							<th on:click={() => toggleSort('Sellers')}>Sellers</th>
							<th on:click={() => toggleSort('Notary')}>Notary</th>
						</tr>
					</thead>
					<tbody>
						{#each displayedTransactions as transaction}
							<tr on:click={() => window.location.href = `/Reports/Transaction?TransactionId=${transaction.TransactionId}`}>
								<td>{transaction.TransactionType || ''}</td>
								<td>{formatTransactionDate(transaction.date_circa, transaction.date_accuracy)}</td>
								<td>{transaction.TotalPrice || ''}</td>
								<td>{transaction.LocationCity || ''}</td>
								<td>{transaction.LocationStateAbbr || ''}</td>
								<td>{transaction.Buyers || ''}</td>
								<td>{transaction.Sellers || ''}</td>
								<td>{transaction.Notary || ''}</td>
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