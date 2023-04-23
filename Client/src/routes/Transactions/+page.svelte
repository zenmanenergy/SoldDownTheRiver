<style>
    @import '/static/FormPages.css';
  </style>
  <script>
    import { onMount } from 'svelte';
    import handleGet from './handleGet.js';
  
    export let transactions = [];
    let isLoading = true;
  
    onMount(async () => {
      transactions = await handleGet();
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
        <ul>
          {#each transactions as transaction}
            <li>
              <a href={`/Transaction?TransactionId=${transaction.TransactionId}`}>
                {transaction.TransactionType} between {transaction.FromHumanId} and {transaction.ToHumanId}
              </a>
            </li>
          {/each}
        </ul>
        <button on:click={addTransaction}>Add Transaction</button>
      </div>
    </div>
  {/if}
  