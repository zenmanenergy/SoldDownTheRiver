<style>
  @import '/static/FormPages.css';
  
</style>
<script>
  
  import moment from 'moment';
  import { onMount } from 'svelte';
  import {handleGetBusinesses} from './handleGetBusinesses.js';
	import {Session} from "../Session.js";

  let businesses = [];
  let isLoading = true;
  
  async function setGetBusinesses(data) {
    businesses = data;
  }
  onMount(async () => {
		await Session.handleSession();
    await Promise.all([
      await handleGetBusinesses(Session.SessionId, setGetBusinesses),
    ]);
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
      <table width=100%>
        <thead>
          <tr>
            <th>Business Name</th>
            <th>Last Modified</th>
          </tr>
        </thead>
        <tbody>
          {#each businesses as business}
            
              <tr style="cursor: pointer;" on:click={location.href=`/Business?BusinessId=${business.BusinessId}`}>
                <td>{business.BusinessName}</td>
                <td>{moment.utc(business.LastModified).local().fromNow()}</td>
              </tr>
            
          {/each}
        </tbody>
      </table>
      
      <button on:click={addBusiness}>Add Business</button>
    </div>
  </div>
{/if}


