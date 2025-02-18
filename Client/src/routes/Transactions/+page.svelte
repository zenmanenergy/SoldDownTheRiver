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

	$: filteredTransactions = Transactions.filter(transaction => {
		const fullTransaction = `${transaction.FirstPartyFirstName} ${transaction.FirstPartyLastName} ${transaction.SecondPartyFirstName} ${transaction.SecondPartyLastName} ${transaction.LocationCity} ${transaction.LocationCounty}`.toLowerCase();
		return fullTransaction.includes(searchQuery.toLowerCase());
	});

	function addTransaction() {
		window.location.href = '/Transaction?transactionId=';
	}
	function truncateText(text, maxLength = 25) {
		if (!text) return "";
		return text.length > maxLength ? text.substring(0, maxLength) + "…" : text;
	}
	function formatTransactionDate(date, accuracy) {
		if (!date) return 'N/A';

		// Use the full string and specify RFC 2822 format
		const parsedDate = moment.utc(date, "ddd, DD MMM YYYY HH:mm:ss [GMT]", true);

		if (!parsedDate.isValid()) {
			console.warn(`Invalid date format received: ${date}`);
			return 'Invalid Date';
		}

		// Format based on accuracy
		switch (accuracy?.toLowerCase()) {
			case 'd': return parsedDate.format('YYYY-MM-DD');
			case 'm': return parsedDate.format('YYYY-MM');
			case 'y': return parsedDate.format('YYYY');
			default: return parsedDate.format('YYYY-MM-DD');
		}
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
				<button class="button is-primary"  on:click={() => addTransaction()}>Add Transaction</button>
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
						<th>Date</th>
						<th>Transaction Type</th>
						<th>Notary</th>
						<th>First Party</th>
						<th>Second Party</th>
						<th>Location</th>
						<th>Total Price</th>
						<th>URL</th>
					</tr>
				</thead>
				<tbody>
					{#each filteredTransactions as transaction}
						<tr style="cursor: pointer;" on:click={() => location.href=`/Transaction?TransactionId=${encodeURIComponent(transaction.TransactionId)}`}>

							<td>{formatTransactionDate(transaction.date_circa, transaction.date_accuracy)}</td>
							<td>{transaction.TransactionType || 'N/A'}</td>
							<td title={`${transaction.NotaryFirstName} ${transaction.NotaryMiddleName || ''} ${transaction.NotaryLastName}`}>
								{truncateText(`${transaction.NotaryFirstName} ${transaction.NotaryMiddleName || ''} ${transaction.NotaryLastName}`)}
							</td>
							<td title={`${transaction.FirstPartyFirstName} ${transaction.FirstPartyMiddleName || ''} ${transaction.FirstPartyLastName}`}>
								{truncateText(`${transaction.FirstPartyFirstName} ${transaction.FirstPartyMiddleName || ''} ${transaction.FirstPartyLastName}`)}
							</td>
							<td title={`${transaction.SecondPartyFirstName} ${transaction.SecondPartyMiddleName || ''} ${transaction.SecondPartyLastName}`}>
								{truncateText(`${transaction.SecondPartyFirstName} ${transaction.SecondPartyMiddleName || ''} ${transaction.SecondPartyLastName}`)}
							</td>
							<td class="location">
								{#if transaction.LocationAddress}
									{transaction.LocationAddress || ''}, {transaction.LocationCity || ''}, {transaction.LocationCounty || ''}, {transaction.LocationStateAbbr || ''}
								{/if}
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
