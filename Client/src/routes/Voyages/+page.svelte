<style>
    @import '/static/FormPages.css';
  </style>
  
  <script>
    import moment from 'moment';
    import { onMount } from 'svelte';
    import handleGet from './handleGet.js';
    import { Session } from "../Session.js";
  
    export let voyages = [];
    let isLoading = true;
  
    onMount(async () => {
      await Session.handleSession();
      voyages = await handleGet(Session.SessionId);
      isLoading = false;
    });
  
    function addVoyage() {
      window.location.href = '/Voyage?VoyageId=';
    }
  </script>
  
  <div class="section">
    {#if isLoading}
      <div class="loading-screen">
        <div class="spinner"></div>
      </div>
    {:else}
      <a href="/AdminMenu">Back to Menu</a>
      <div class="ActionBox">
        <h3 class="title is-2">List of Voyages</h3>
        <ul>
          {#each voyages as voyage}
            <li>
              <a href={`/Voyage?VoyageId=${voyage.VoyageId}`}>
                {voyage.VoyageName}
              </a>
            </li>
          {/each}
        </ul>
        <button on:click={addVoyage}>Add Voyage</button>
      </div>
    {/if}
  </div>
  