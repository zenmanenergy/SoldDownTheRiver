<style>
  @import '/static/FormPages.css';
</style>
<script>
    import moment from 'moment';
    import { onMount } from 'svelte';
    import handleGet from './handleGet.js';
	  import {Session} from "../Session.js";
  
    export let locations = [];
    let isLoading = true;
  
    onMount(async () => {
		  await Session.handleSession();
      locations = await handleGet(Session.SessionId);
      isLoading = false;
    });
  
    function addLocation() {
      window.location.href = '/Location?LocationId=';
    }
    function go(LocationId) {
      window.location.href = `/Location?LocationId=`+LocationId;
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
      <table width=100%>
        <thead>
          <tr>
            <th>City</th>
            <th>State</th>
            <th>Country</th>
            <th>Last Modified</th>
          </tr>
        </thead>
        <tbody>
          {#each locations as location}
            <tr style="cursor: pointer;" on:click={go(`${location.LocationId}`)}>
              <td>{location.City}</td>
              <td>{location.State}</td>
              <td>{location.Country}</td>
              <td>{moment(location.LastModified).fromNow()}</td>
            </tr>
          {/each}
        </tbody>
      </table>
      <button on:click={addLocation}>Add Location</button>
    </div>
  </div>
  
  {/if}
  