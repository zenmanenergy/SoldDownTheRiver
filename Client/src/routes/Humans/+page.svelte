<script>
    import { onMount } from 'svelte';
    import handleGet from './handleGet.js';
  
    export let humans = [];
    let isLoading = true;
  
    onMount(async () => {
      humans = await handleGet();
      isLoading = false;
    });
  
    function addHuman() {
      window.location.href = '/Human?HumanId=';
    }
  </script>
  {#if isLoading}
  
    <div class="loading-screen">
      <div class="spinner"></div>
    </div>
  {:else}
    <div>
      <h1>List of Humans</h1>
      <ul>
        {#each humans as human}
          <li>
            <a href={`/Human?HumanId=${human.HumanId}`}>
              {human.FirstName} {human.LastName}
            </a>
          </li>
        {/each}
      </ul>
      <button on:click={addHuman}>Add Human</button>
    </div>
  {/if}