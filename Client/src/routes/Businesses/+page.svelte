<style>
  @import '/static/FormPages.css';
</style>
<script>
  import { onMount } from 'svelte';
  import handleGet from './handleGet.js';

  export let businesses = [];
  let isLoading = true;

  onMount(async () => {
    businesses = await handleGet();
    isLoading = false;
  });

  function addBusiness() {
    window.location.href = '/Business?BusinessId=';
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
      <h3 class="title is-2">List of Businesses</h3>
      <ul>
        {#each businesses as business}
          <li>
            <a href={`/Business?BusinessId=${business.BusinessId}`}>
              {business.BusinessName}
            </a>
          </li>
        {/each}
      </ul>
      <button on:click={addBusiness}>Add Business</button>
    </div>
  </div>
{/if}


