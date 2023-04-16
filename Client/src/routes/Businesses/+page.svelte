<script>
  import { onMount } from 'svelte';
  import handleGet from './handleGet.js';

  export let businesses = [];

  onMount(async () => {
    businesses = await handleGet();
  });

  function addBusiness() {
    window.location.href = '/Business?BusinessId=';
  }
</script>

<div>
  <h1>List of Businesses</h1>
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
