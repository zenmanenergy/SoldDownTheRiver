<style>
    @import '/static/FormPages.css';
  </style>
  
  <script>
    import moment from 'moment';
    import { onMount } from 'svelte';
    import handleGet from './handleGet.js';
    import { Session } from "../Session.js";
  
    export let ships = [];
    let isLoading = true;
  
    onMount(async () => {
      await Session.handleSession();
      ships = await handleGet(Session.SessionId);
      isLoading = false;
    });
  
    function addShip() {
      window.location.href = '/Ship?ShipId=';
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
        <h3 class="title is-2">List of Ships</h3>
        <ul>
          {#each ships as ship}
            <li>
              <a href={`/Ship?ShipId=${ship.ShipId}`}>
                {ship.ShipName}
              </a>
            </li>
          {/each}
        </ul>
        <button on:click={addShip}>Add Ship</button>
      </div>
    </div>
  {/if}
  