<!-- src/routes/Voyages/+page.svelte -->
<style>
    @import '/static/FormPages.css';
  </style>
  <script>
    import moment from 'moment';
    import { onMount } from 'svelte';
    import { handleSave } from './handleSave.js';
    import { handleDelete } from './handleDelete.js';
    import { handleGet } from './handleGet.js';
    import { handleGetShips } from './handleGetShips.js';
    import { Session } from '../Session.js';
  
    let VoyageId = '';
    let ShipId = '';
    let StartLocationId = '';
    let EndLocationId = '';
    let StartDate = null;
    let EndDate = null;
    let Notes = '';
    let Voyage={VoyageId:"", ShipId:"", StartLocationId:"", EndLocationId:"", StartDate:null, EndDate:null, Notes:""};
    let Ships=[]
  
    let formValid = false;
    let isLoading = true;
  
    async function setVoyage(data) {

      Voyage.VoyageId = data.VoyageId || "";
      Voyage.ShipId = data.ShipId || "";
      Voyage.StartLocationId = data.StartLocationId || "";
      Voyage.EndLocationId = data.EndLocationId || "";
      if (data.StartDate){
        Voyage.StartDate = moment(data.StartDate).format("YYYY-MM-DDTHH:mm:ss")||"";
      }
      if (data.EndDate){
        Voyage.EndDate = moment(data.EndDate).format("YYYY-MM-DDTHH:mm:ss")||"";
      }
      Voyage.Notes = data.Notes || "";
      
    }
    async function setShips(data) {
      Ships = data;
    }
    $: {
      formValid = Voyage.ShipId;
    }
  
    onMount(async () => {
      await Session.handleSession();
      const urlParams = new URLSearchParams(window.location.search);
      VoyageId = urlParams.get('VoyageId') || '';
      
      await Promise.all([
				handleGet(Session.SessionId, VoyageId, setVoyage),
        handleGetShips(Session.SessionId, setShips)

			]);
      isLoading = false;
    });
  </script>
  
  {#if isLoading}
    <div class="loading-screen">
      <div class="spinner"></div>
    </div>
  {:else}
    <div class="section">
      <a href="/Voyages">Back to Voyages</a>
      <div class="ActionBox">
        <form>
          <h3 class="title is-2">Add a Voyage</h3>
          <input type="hidden" bind:value={Voyage.VoyageId} />
  
          <div class="field">
            <label class="label" for="FromBusinessId">From:</label>
            <div class="control">
              <select class="input" id="ShipId" bind:value={Voyage.ShipId} required>
                <option value=""></option>
                {#each Ships as Ship}
                  <option value={Ship.ShipId}>{Ship.ShipName}</option>
                {/each}
              </select>
            </div>
          </div>
          <div class="field">
            <label class="label" for="StartLocationId">Start Location ID</label>
            <div class="control">
              <input class="input" type="text" id="StartLocationId" placeholder="Enter Start Location ID" bind:value={Voyage.StartLocationId} />
            </div>
          </div>
  
          <div class="field">
            <label class="label" for="EndLocationId">End Location ID</label>
            <div class="control">
              <input class="input" type="text" id="EndLocationId" placeholder="Enter End Location ID" bind:value={Voyage.EndLocationId} />
            </div>
          </div>
  
          <div class="field">
            <label class="label" for="StartDate">Start Date</label>
            <div class="control">
              <input class="input" type="date" id="StartDate" bind:value={Voyage.StartDate} />
            </div>
          </div>
          <div class="field">
            <label class="label" for="EndDate">End Date</label>
            <div class="control">
              <input class="input" type="date" id="EndDate" bind:value={Voyage.EndDate} />
            </div>
          </div>
          <div class="field">
            <label class="label" for="Notes">Notes</label>
            <div class="control">
              <input class="input" type="text" id="Notes" placeholder="Enter Notes" bind:value={Voyage.Notes}/>
            </div>
          </div>
          <div class="field">
            <div class="control">
              <button class="button is-primary" type="button" on:click={() =>   handleSave(Session.SessionId,Voyage,formValid   ) }> Save</button>
              {#if VoyageId.length}
                <button class="button is-danger" type="button" on:click={() => handleDelete(Session.SessionId, VoyageId)}>Delete</button>
              {/if}
            </div>
          </div>
        </form>
      </div>
    </div>
  {/if}
  