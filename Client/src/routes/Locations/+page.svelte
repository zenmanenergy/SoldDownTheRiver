<style>
  @import '/static/FormPages.css';
</style>
<script>
    import { onMount } from 'svelte';
    import handleGet from './handleGet.js';
  
    export let locations = [];
    let isLoading = true;
  
    onMount(async () => {
      locations = await handleGet();
      isLoading = false;
    });
  
    function addLocation() {
      window.location.href = '/Location?LocationId=';
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
      <h3 class="title is-2">List of Locations</h3>
      <ul>
        {#each locations as location}
          <li>
            <a href={`/Location?LocationId=${location.LocationId}`}>
              {location.City}, {location.State}, {location.Country}
            </a>
          </li>
        {/each}
      </ul>
      <button on:click={addLocation}>Add Location</button>
    </div>
  </div>
  {/if}
  