<style>
  @import '/static/FormPages.css';
</style>
<script>
    import { onMount } from 'svelte';
    import handleGet from './handleGet.js';
	  import {Session} from "../Session.js";
  
    export let humans = [];
    let isLoading = true;
  
    onMount(async () => {
      await Session.handleSession();
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
  <div class="section">
    <a href="/AdminMenu">Back to Menu</a>
    <div class="ActionBox">
      <h3 class="title is-2">List of Humans</h3>
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
    </div>
  {/if}