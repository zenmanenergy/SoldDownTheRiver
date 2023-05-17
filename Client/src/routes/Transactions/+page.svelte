<style>
    @import '/static/FormPages.css';
  </style>
  <script>
    import moment from 'moment';
    import { onMount } from 'svelte';
    import {handleGetTransactions} from './handleGetTransactions.js';
	  import {Session} from "../Session.js";
  
    let Transactions = [];
    let isLoading = true;
  
    async function setTransactions(data) {
      Transactions = data
    }
    onMount(async () => {
		await Session.handleSession();
      await Promise.all([
				handleGetTransactions(Session.SessionId,setTransactions),
			]);
      isLoading = false;
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
      <table width=100%>
        <thead>
          <tr>
            <th>Business Name</th>
            <th>Transaction Date</th>
            <th>Last Modified</th>
          </tr>
        </thead>
        <tbody>
          {#each Transactions as transaction}
            <tr style="cursor: pointer;" on:click={location.href=`/Transaction?TransactionId=${transaction.TransactionId}`}>
              
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
  