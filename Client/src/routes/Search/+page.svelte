




<style>
   @import '/static/FormPages.css';

   .loading-overlay {
	   position: fixed;
	   top: 0;
	   left: 0;
	   width: 100vw;
	   height: 100vh;
	   background: rgba(0,0,0,0.3);
	   z-index: 1000;
	   display: flex;
	   align-items: center;
	   justify-content: center;
   }
   .loading-modal {
	   background: #fff;
	   border-radius: 12px;
	   box-shadow: 0 2px 16px rgba(0,0,0,0.15);
	   padding: 2.5em 2.5em 2em 2.5em;
	   min-width: 260px;
	   min-height: 120px;
	   display: flex;
	   flex-direction: column;
	   align-items: center;
   }
   .loading-progress {
	   margin-top: 1.5em;
	   font-size: 1.2em;
	   color: #333;
   }
</style>

<script>
let searchType = 'People';
let searchQuery = '';
let prevSearchType = searchType;
let prevSearchQuery = searchQuery;
let justLoaded = true;

	import moment from 'moment';
	import { onMount, afterUpdate } from 'svelte';
	import { handleSearchHumans } from './handleSearchHumans.js';
	import { handleSearchShips } from './handleSearchShips.js';
	import { handleSearchTransactions } from './handleSearchTransactions.js';
	import { handleSearchLocations } from './handleSearchLocations.js';

	let Humans = [];
	let Ships = [];
	let Transactions = [];
	let filteredHumans = [];
	let filteredShips = [];
	let Locations = [];
	let filteredTransactions = [];
	let filteredLocations = [];

	let isLoading = true;
	let loadingPercent = 0;
	let loadingInterval;
	let lastIsLoading = undefined;

	import { onDestroy } from 'svelte';

	// Watch isLoading and manage the interval
	$: if (isLoading !== lastIsLoading) {
		if (isLoading) {
			loadingPercent = 0;
			clearInterval(loadingInterval);
			loadingInterval = setInterval(() => {
				loadingPercent = Math.round(loadingPercent + 100 / (15 * 10)); // 15 seconds, update every 100ms
				if (loadingPercent >= 99) {
					loadingPercent = 99;
				}
			}, 100);
		} else {
			loadingPercent = 100;
			clearInterval(loadingInterval);
		}
		lastIsLoading = isLoading;
	}

	onDestroy(() => {
		clearInterval(loadingInterval);
	});


	let currentPage = 1;
	let initialPageFromUrl = 1;
	let initialPageHandled = false;
	let isInitialLoad = true;
	let itemsPerPage = 50;
	let totalPages = 1;

	let sortColumn = 'LastName';
	let sortAscending = true;

	const searchTypes = ['People', 'Transactions', 'Ships', 'Locations'];


	// Helper to update the URL query params, including page
       function updateUrlParams() {
	       justLoaded = false;
	       const params = new URLSearchParams(window.location.search);
	       params.set('type', searchType.toLowerCase());
	       params.set('q', searchQuery);
	       params.set('page', currentPage);
	       const newUrl = `${window.location.pathname}?${params.toString()}`;
	       window.history.replaceState({}, '', newUrl);
       }

	// Update only the page param in the URL
	function updatePageParam() {
		const params = new URLSearchParams(window.location.search);
		params.set('page', currentPage);
		const newUrl = `${window.location.pathname}?${params.toString()}`;
		window.history.replaceState({}, '', newUrl);
	}

	// On mount, read params and set initial state (including page)
	onMount(async () => {
		function syncFromUrl() {
			const params = new URLSearchParams(window.location.search);
			const typeParam = params.get('type');
			const qParam = params.get('q');
			const pageParam = params.get('page');
			if (typeParam && searchTypes.map(t => t.toLowerCase()).includes(typeParam)) {
				searchType = searchTypes.find(t => t.toLowerCase() === typeParam);
			}
			if (qParam !== null) {
				searchQuery = qParam;
			}
			if (pageParam !== null && !isNaN(parseInt(pageParam))) {
				initialPageFromUrl = Math.max(1, parseInt(pageParam));
				currentPage = initialPageFromUrl;
			} else {
				initialPageFromUrl = 1;
				currentPage = 1;
			}
			initialPageHandled = false;
			isInitialLoad = true;
		}

		syncFromUrl();
		await handleSearchHumans(setHumans);
		await handleSearchShips(setShips);
		await handleSearchTransactions(setTransactions);
		await handleSearchLocations(setLocations);
		isLoading = false;

		// Listen for browser navigation (back/forward)
		const popHandler = () => {
			syncFromUrl();
		};
		window.addEventListener('popstate', popHandler);

		// Cleanup
		return () => {
			window.removeEventListener('popstate', popHandler);
		};
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
	function setLocations(data) {
		Locations = data;
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

		totalPages = Math.max(1, Math.ceil(filteredHumans.length / itemsPerPage));
	
	}



	// SSR-safe: Remove all window usage from reactive blocks. All URL reading is handled in onMount and event handlers only.
	

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
				ship.Captains,
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
			if (currentPage > totalPages) currentPage = totalPages;
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
			if (currentPage > totalPages) currentPage = totalPages;
		}
	}

	// Reactive statement for filtering locations
	$: {
		filteredLocations = Locations.filter(location => {
			const search = searchQuery.toLowerCase();
			const searchWords = search.trim().split(/\s+/).filter(word => word.length > 0);

			// If no search words, show all locations
			if (searchWords.length === 0) {
				return true;
			}

			const values = [
				location.LocationType,
				location.Address,
				location.City,
				location.County,
				location.State,
				location.StateAbbr,
				location.Description
			];

			const searchableText = values.join(' ').toLowerCase();

			return searchWords.every(word => searchableText.includes(word));
		});

		// Sort the filtered locations
		filteredLocations.sort((a, b) => {
			let valueA = a[sortColumn] ?? '';
			let valueB = b[sortColumn] ?? '';

			// Convert to lowercase for case-insensitive sorting
			if (typeof valueA === 'string') valueA = valueA.toLowerCase();
			if (typeof valueB === 'string') valueB = valueB.toLowerCase();

			if (valueA < valueB) return sortAscending ? -1 : 1;
			if (valueA > valueB) return sortAscending ? 1 : -1;
			return 0;
		});

		if (searchType === 'Locations') {
			totalPages = Math.max(1, Math.ceil(filteredLocations.length / itemsPerPage));
			if (currentPage > totalPages) currentPage = totalPages;
		}
	}

	$: displayedHumans = filteredHumans.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);
	$: displayedShips = filteredShips.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);
	$: displayedTransactions = filteredTransactions.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);
	$: displayedLocations = filteredLocations.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

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
		   // Reset page to 1 if searchType or searchQuery changes (and not justLoaded)
		   if (!justLoaded && (searchType !== prevSearchType || searchQuery !== prevSearchQuery)) {
			   console.log('[debug] Resetting currentPage to 1 and updating URL to page=1. justLoaded:', justLoaded, 'searchType:', searchType, 'prevSearchType:', prevSearchType, 'searchQuery:', searchQuery, 'prevSearchQuery:', prevSearchQuery);
			   currentPage = 1;
			   // Force page=1 in URL
			   const params = new URLSearchParams(window.location.search);
			   params.set('page', '1');
			   const newUrl = `${window.location.pathname}?${params.toString()}`;
			   window.history.replaceState({}, '', newUrl);
			   prevSearchType = searchType;
			   prevSearchQuery = searchQuery;
		   }

		   if (searchType === 'People' && Humans.length === 0 && !isLoading) {
			   isLoading = true;
			   handleSearchHumans(setHumans).then(() => {
				   isLoading = false;
				   // Now that totalPages is known, clamp currentPage if needed
				   syncFromUrl();
				   // Mark as loaded after sync
				   setTimeout(() => {
					   justLoaded = false;
					   prevSearchType = searchType;
					   prevSearchQuery = searchQuery;
					   console.log('[debug] justLoaded set to false, prevSearchType:', prevSearchType, 'prevSearchQuery:', prevSearchQuery);
				   }, 0);
			   });
		} else if (searchType === 'Ships' && Ships.length === 0 && !isLoading) {
			isLoading = true;
			handleSearchShips(setShips).then(() => {
				isLoading = false;
			});
		} else if (searchType === 'Transactions' && Transactions.length === 0 && !isLoading) {
			isLoading = true;
			handleSearchTransactions(setTransactions).then(() => {
				isLoading = false;
			});
		} else if (searchType === 'Locations' && Locations.length === 0 && !isLoading) {
			isLoading = true;
			handleSearchLocations(setLocations).then(() => {
				isLoading = false;
			});
		}
	}

	// Clear search query when search type changes
	// $: {
	// 	if (searchType) {
	// 		searchQuery = '';
	// 		console.log("SEARCH TYPE")
	// 	}
	// }
</script>

{#if isLoading}
   <div class="loading-overlay">
	   <div class="loading-modal">
		   <div class="spinner"></div>
		   <div class="loading-progress">
			   Loading... {loadingPercent}%
		   </div>
	   </div>
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
							<select id="searchType" bind:value={searchType} on:change={updateUrlParams}>
								{#each searchTypes as type}
									<option value={type}>{type}</option>
								{/each}
							</select>
						</div>
					</div>
				</div>
				<div class="field">
					<div class="control">
						<input class="input" type="text" bind:value={searchQuery} placeholder="Search" on:input={updateUrlParams} />
					</div>
				</div>
			</form>
			
			<!-- Results count display -->
			<div class="results-count" style="margin: 1rem 0; font-weight: bold; color: #363636;">
				{#if searchType === 'People'}
					Showing {filteredHumans.length} result{filteredHumans.length !== 1 ? 's' : ''}
				{:else if searchType === 'Ships'}
					Showing {filteredShips.length} result{filteredShips.length !== 1 ? 's' : ''}
				{:else if searchType === 'Transactions'}
					Showing {filteredTransactions.length} result{filteredTransactions.length !== 1 ? 's' : ''}
				{:else if searchType === 'Locations'}
					Showing {filteredLocations.length} result{filteredLocations.length !== 1 ? 's' : ''}
				{/if}
			</div>
			
			{#if searchType === 'People'}
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
							<tr on:click={() => window.location.href = `/Reports/Human?HumanId=${human.HumanId}`}>
								<td>{human.FirstName || ''}{' ' & human.MiddleName || ''}</td>
								<td>{human.LastName || ''}</td>
								<td>{formatBirthDate(human.BirthDate, human.BirthDateAccuracy) || ''}</td>
								<td>{human.RacialDescriptor || ''}</td>
								<td>{human.Sex || ''}</td>
								<td>{human.Roles.length > 0 ? human.Roles.join(', ') : ''}</td>
							</tr>
						{/each}
					</tbody>
				</table>
				
				<div class="pagination">
					<button on:click={() => { currentPage = Math.max(currentPage - 1, 1); updatePageParam(); }} disabled={currentPage === 1}>
						Previous
					</button>
					<span>{currentPage} / {totalPages}</span>
					<button on:click={() => { currentPage = Math.min(currentPage + 1, totalPages); updatePageParam(); }} disabled={currentPage === totalPages}>
						Next
					</button>
				</div>
			{:else if searchType === 'Ships'}
				<table class="table is-striped is-hoverable is-fullwidth">
					<thead>
						<tr>
							<th on:click={() => toggleSort('ShipName')}>Ship Name</th>
							<th on:click={() => toggleSort('ShipType')}>Ship Type</th>
							<th on:click={() => toggleSort('Captains')}>Captains</th>
						</tr>
					</thead>
					<tbody>
						{#each displayedShips as ship}
							<tr on:click={() => window.location.href = `/Reports/Ship?ShipId=${ship.ShipId}`}>
								<td>{ship.ShipName || ''}</td>
								<td>{ship.ShipType || ''}</td>
								<td>{ship.Captains || ''}</td>
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
			{:else if searchType === 'Locations'}
				<table class="table is-striped is-hoverable is-fullwidth">
					<thead>
						<tr>
							<th on:click={() => toggleSort('Address')}>Address</th>
							<th on:click={() => toggleSort('City')}>City</th>
							<th on:click={() => toggleSort('State')}>State</th>
							<th on:click={() => toggleSort('LocationType')}>Location Type</th>
						</tr>
					</thead>
					<tbody>
						{#each displayedLocations as location}
							<tr on:click={() => window.location.href = `/Reports/Location?LocationId=${location.LocationId}`}>
								<td>{location.Address || ''}</td>
								<td>{location.City || ''}</td>
								<td>{location.State || ''}</td>
								<td>{location.LocationType || ''}</td>
								
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