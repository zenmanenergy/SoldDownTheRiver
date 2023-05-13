<!-- src/routes/Ships/+page.svelte -->
<style>
    @import '/static/FormPages.css';
  </style>
  <script>
    import moment from 'moment';
    import { onMount } from 'svelte';
    import { handleSave } from './handleSave.js';
    import { handleDelete } from './handleDelete.js';
    import { handleGet } from './handleGet.js';
    import { Session } from "../Session.js";
  
    let ShipId = "";
    let BuildDate = null;
    let Notes = "";
    let ShipType = "";
    let Size = "";
    let Ship={ShipId:"", ShipName:"", BuildDate:null, Notes:"", ShipType:"", Size:""};
  
    let formValid = false;
    let isLoading = true;
  
    async function setShip(data) {
      console.log(data.BuildDate)
      Ship.ShipId = data.ShipId || "";
      Ship.ShipName = data.ShipName || "";
      if (data.BuildDate){
        Ship.BuildDate = moment(data.BuildDate).format("YYYY-MM-DDTHH:mm:ss")||"";
      }
      Ship.Notes = data.Notes || "";
      Ship.ShipType = data.ShipType || "";
      Ship.Size = data.Size || "";
      
      
      console.log("Ship", Ship)
      console.log("Ship.ShipId.length", Ship.ShipId.length)
    }
  
    $: {
      formValid = Ship.ShipName;
    }
  
    onMount(async () => {
      await Session.handleSession();
      const urlParams = new URLSearchParams(window.location.search);
      ShipId = urlParams.get("ShipId") || "";
      handleGet(Session.SessionId, ShipId, setShip);
  
      console.log("ShipId", ShipId)
      isLoading = false;
    });
  </script>
  
  
  {#if isLoading}
    <div class="loading-screen">
      <div class="spinner"></div>
    </div>
  {:else}
  
    <div class="section">
      <a href="/Ships">Back to Ships</a>
      <div class="ActionBox">
        <form>
          <h3 class="title is-2">Add a Ship</h3>
          <input type="hidden" bind:value={Ship.ShipId} />
  
          <div class="field">
            <label class="label" for="ShipName">Ship Name</label>
            <div class="control">
              <input class="input" type="text" id="ShipName" placeholder="Enter ShipName" bind:value={Ship.ShipName} required />
            </div>
          </div>

          <div class="field">
            <label class="label" for="BuildDate">Build Date</label>
            <div class="control">
              <input class="input" type="datetime" id="BuildDate" placeholder="Enter Build Date" bind:value={Ship.BuildDate} />
            </div>
          </div>
  
          <div class="field">
            <label class="label" for="Notes">Notes</label>
            <div class="control">
              <input class="input" type="text" id="Notes" placeholder="Enter Notes" bind:value={Ship.Notes} />
            </div>
          </div>
  
          <div class="field">
            <label class="label" for="ShipType">Ship Type</label>
            <div class="control">
              <input class="input" type="text" id="ShipType" placeholder="Enter Ship Type" bind:value={Ship.ShipType} />
            </div>
          </div>
  
          <div class="field">
            <label class="label" for="Size">Size</label>
            <div class="control">
              <input class="input" type="text" id="Size" placeholder="Enter Size" bind:value={Ship.Size} />
            </div>
          </div>
  
          <div class="field">
            <div class="control">
              <button class="button is-primary" type="button" on:click={() => handleSave(Session.SessionId, Ship, formValid)}>Save</button>
              {#if Ship.ShipId.length}
                <button class="button is-danger" type="button" on:click={() => handleDelete(Session.SessionId, Ship.ShipId)}>Delete</button>
              {/if}
            </div>
          </div>
        </form>
        </div>
        </div>
        {/if}
        