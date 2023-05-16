<style>
  @import '/static/FormPages.css';
</style>
<script>
    import moment from 'moment';
    import { onMount } from 'svelte';
    import {handleGet} from './handleGet.js';
	  import {Session} from "../Session.js";
  
    let Locations = [];
    let isLoading = true;
  
    async function setLocations(data) {
      Locations=data
      
    }
    onMount(async () => {
		  await Session.handleSession();
      await Promise.all([
				await handleGet(Session.SessionId,setLocations)
				
			]);
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
          {#each Locations as location}
            <tr style="cursor: pointer;" on:click={go(`${location.LocationId}`)}>
              <td>{location.City}</td>
              <td>{location.State}</td>
              <td>{location.Country}</td>
              <td>{moment.utc(location.LastModified).local().fromNow()}</td>
            </tr>
          {/each}
        </tbody>
      </table>
      <button on:click={addLocation}>Add Location</button>
    </div>
  </div>
  
  {/if}
  