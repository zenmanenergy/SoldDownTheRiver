<style>
  @import '/static/FormPages.css';
</style>
<script>
    import moment from 'moment';
    import { onMount } from 'svelte';
	  import {Session} from "../Session.js";
    import { handleGetHumans } from './handleGetHumans.js';
  
    let Humans = [];
    let isLoading = true;
    
    async function setHumans(data) {
      Humans = data;
    }
    onMount(async () => {
      await Session.handleSession();
      await Promise.all([
        await handleGetHumans(Session.SessionId, setHumans)
          
      ]);
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
      <table width=100%>
        <thead>
          <tr>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Last Modified</th>
          </tr>
        </thead>
        <tbody>
          {#each Humans as human}
            <tr style="cursor: pointer;" on:click={location.href=`/Human?HumanId=${human.HumanId}`}>
              <td>{human.FirstName}</td>
              <td>{human.LastName}</td>
              <td>{moment.utc(human.LastModified).local().fromNow()}</td>
            </tr>
          {/each}
        </tbody>
      </table>
      <button on:click={addHuman}>Add Human</button>
    </div>
  </div>
  
  {/if}