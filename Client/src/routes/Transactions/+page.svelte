<style>
	@import '/static/FormPages.css';

	table {
		width: 100%;
		border-collapse: collapse;
	}

	th, td {
		padding: 8px;
		text-align: left;
		border-bottom: 1px solid #ddd;
	}

	th {
		background-color: #f2f2f2;
		white-space: nowrap;
		cursor: pointer;
	}

	th:hover {
		background-color: #e0e0e0;
	}

	td {
		white-space: nowrap;
	}

	.location {
		white-space: normal;
	}
</style>

<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleGetTransactions } from './handleGetTransactions.js';
	import { Session } from "../Session.js";

	let Transactions = [];
	let filteredTransactions = [];
	let isLoading = true;
	let searchQuery = '';

	let sortColumn = 'date_circa';
	let sortAscending = true;

	async function setTransactions(data) {
		Transactions = [...data]; // Ensure reactivity
	}

	onMount(async () => {
		await Session.handleSession();
		if (Session.SessionId) {
			await handleGetTransactions(Session.SessionId, setTransactions);
		}
		isLoading = false;
	});

	function formatTransactionDate(date, accuracy) {
		if (!date) return 'N/A';

		const parsedDate = moment.utc(date, "ddd, DD MMM YYYY HH:mm:ss [GMT]", true);

		if (!parsedDate.isValid()) {
			console.warn(`Invalid date format received: ${date}`);
			return 'Invalid Date';
		}

		switch (accuracy?.toLowerCase()) {
			case 'd': return parsedDate.format('YYYY-MM-DD');
			case 'm': return parsedDate.format('YYYY-MM');
			case 'y': return parsedDate.format('YYYY');
			default: return parsedDate.format('YYYY-MM-DD');
		}
	}

	function truncateText(text, maxLength = 25) {
		if (!text) return "";
		return text.length > maxLength ? text.substring(0, maxLength) + "…" : text;
	}

	function toggleSort(column) {
		if (sortColumn === column) {
			sortAscending = !sortAscending;
		} else {
			sortColumn = column;
			sortAscending = true;
		}
	}

	// Updated filteredTransactions to include transactionId and nola_id in the search string
	$: filteredTransactions = Transactions
		.filter(transaction => {
			const fullTransaction = `
				${transaction.FirstPartyFirstName} 
				${transaction.FirstPartyLastName} 
				${transaction.SecondPartyFirstName} 
				${transaction.SecondPartyLastName} 
				${transaction.LocationCity} 
				${transaction.LocationCounty} 
				${transaction.TransactionId} 
				${transaction.nola_id}
			`.toLowerCase();
			return fullTransaction.includes(searchQuery.toLowerCase());
		})
		.sort((a, b) => {
			let valueA = a[sortColumn] ?? '';
			let valueB = b[sortColumn] ?? '';

			// Handle sorting for dates
			if (sortColumn === 'date_circa') {
				valueA = a.date_circa ? new Date(a.date_circa) : new Date(0);
				valueB = b.date_circa ? new Date(b.date_circa) : new Date(0);
			}

			// Handle sorting for numbers
			if (sortColumn === 'TotalPrice') {
				valueA = parseFloat(a.TotalPrice) || 0;
				valueB = parseFloat(b.TotalPrice) || 0;
			}

			// Convert strings to lowercase for case-insensitive sorting
			if (typeof valueA === 'string') valueA = valueA.toLowerCase();
			if (typeof valueB === 'string') valueB = valueB.toLowerCase();

			if (valueA < valueB) return sortAscending ? -1 : 1;
			if (valueA > valueB) return sortAscending ? 1 : -1;
			return 0;
		});
	
	function addTransaction() {
		window.location.href = '/Transaction?transactionId=';
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
				<h3 class="title is-2">List of Transactions</h3>
				<button class="button is-primary" on:click={addTransaction}>Add Transaction</button>
			</div>
			
			<form>
				<div class="field">
					<div class="control">
						<input class="input" type="text" bind:value={searchQuery} placeholder="Search by name or location" />
					</div>
				</div>
			</form>
			<table>
				<thead>
					<tr>
						<th on:click={() => toggleSort('date_circa')}>Date</th>
						<th on:click={() => toggleSort('TransactionType')}>Transaction Type</th>
						<th on:click={() => toggleSort('NotaryFirstName')}>Notary</th>
						<th on:click={() => toggleSort('FirstPartyFirstName')}>First Party</th>
						<th on:click={() => toggleSort('SecondPartyFirstName')}>Second Party</th>
						<th on:click={() => toggleSort('LocationCity')}>Location</th>
						<th on:click={() => toggleSort('TotalPrice')}>Total Price</th>
						<th>URL</th>
					</tr>
				</thead>
				<tbody>
					{#each filteredTransactions as transaction}
						<tr style="cursor: pointer;" on:click={() => location.href=`/Transaction?TransactionId=${encodeURIComponent(transaction.TransactionId)}`}>
							<td>{formatTransactionDate(transaction.date_circa, transaction.date_accuracy)}</td>
							<td>{transaction.TransactionType || 'N/A'}</td>
							<td title={`${transaction.NotaryFirstName} ${transaction.NotaryMiddleName || ''} ${transaction.NotaryLastName}`} >
								{truncateText(`${transaction.NotaryFirstName} ${transaction.NotaryMiddleName || ''} ${transaction.NotaryLastName}`)}
							</td>
							<td title={`${transaction.FirstPartyFirstName} ${transaction.FirstPartyMiddleName || ''} ${transaction.FirstPartyLastName}`} >
								{truncateText(`${transaction.FirstPartyFirstName} ${transaction.FirstPartyMiddleName || ''} ${transaction.FirstPartyLastName}`)}
							</td>
							<td title={`${transaction.SecondPartyFirstName} ${transaction.SecondPartyMiddleName || ''} ${transaction.SecondPartyLastName}`} >
								{truncateText(`${transaction.SecondPartyFirstName} ${transaction.SecondPartyMiddleName || ''} ${transaction.SecondPartyLastName}`)}
							</td>
							<td class="location">
								{transaction.LocationAddress ? `${transaction.LocationAddress}, ` : ''}{transaction.LocationCity || ''}, {transaction.LocationCounty || ''}, {transaction.LocationStateAbbr || ''}
							</td>
							<td>{transaction.TotalPrice ? `$${transaction.TotalPrice.toFixed(2)}` : ''}</td>
							<td>
								{#if transaction.URL}
									<a href={transaction.URL} target="_blank">View</a>
								{/if}
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
{/if}
