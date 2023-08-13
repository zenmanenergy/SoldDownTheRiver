<style>
	@import '/static/FormPages.css';
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
		Transactions = data;
	}

	onMount(async () => {
		await Session.handleSession();
		await Promise.all([
			handleGetTransactions(Session.SessionId, setTransactions),
		]);
		isLoading = false;
	});

	$: filteredTransactions = Transactions.filter(transaction => {
		const fullTransaction = `${transaction.FromBusinessName} ${transaction.ToBusinessName}`.toLowerCase();
		return fullTransaction.includes(searchQuery.toLowerCase());
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
			<h3 class="title is-2">List of Transactions</h3>
			<button on:click={addTransaction}>Add Transaction</button>
			<form>
				<div class="field">
					<div class="control">
						<input class="input" type="text" bind:value={searchQuery} placeholder="Search by business name" />
					</div>
			
				</div>
			</form>
			<table width=100%>
				<thead>
					<tr>
						<th>Business Name</th>
						<th>Transaction Date</th>
						<th>Last Modified</th>
					</tr>
				</thead>
				<tbody>
					{#each filteredTransactions as transaction}
						<tr style="cursor: pointer;" on:click={() => location.href=`/Transaction?TransactionId=${transaction.TransactionId}`}>
							<td>{transaction.FromBusinessName}--->{transaction.ToBusinessName}</td>
							<td>{moment(transaction.TransactionDate).format('MMMM Do YYYY, h:mm:ss a')}</td>
							<td>{moment.utc(transaction.LastModified).local().fromNow()}</td>
						</tr>
					{/each}
				</tbody>
			</table>
			<button on:click={addTransaction}>Add Transaction</button>
		</div>
	</div>
{/if}
