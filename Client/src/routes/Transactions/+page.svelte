<style>
    @import '/static/FormPages.css';
  </style>
  <script>
    import moment from 'moment';
    import { onMount } from 'svelte';
    import handleGet from './handleGet.js';
	  import {Session} from "../Session.js";
  
    export let transactions = [];
    let isLoading = true;
  
    onMount(async () => {
		await Session.handleSession();
      transactions = await handleGet(Session.SessionId);
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
            <th>Transaction ID</th>
            <th>Business Name</th>
            <th>Transaction Date</th>
            <th>Last Modified</th>
          </tr>
        </thead>
        <tbody>
          {#each transactions as transaction}
            <tr style="cursor: pointer;" on:click={location.href=`/Transaction?TransactionId=${transaction.TransactionId}`}>
              <td>{transaction.TransactionId}</td>
              <td>{transaction.BusinessName}</td>
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
  