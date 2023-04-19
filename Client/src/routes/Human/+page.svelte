<!-- src/routes/Humans/+page.svelte -->
<style>
  @import '/static/FormPages.css';
</style>
<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { handleSave } from './handleSave.js';
  import { handleDelete } from './handleDelete.js';
  import { handleGet } from './handleGet.js';
  import { handleGetAKA } from './handleGetAKA.js';
  import { handleSaveAkaName } from './handleSaveAkaName.js';
  import { handleDeleteAkaName } from './handleDeleteAkaName.js';
  
  let HumanId = '';
  let FirstName = '';
  let MiddleName = '';
  let LastName = '';
  let StartYear = '';
  let EndYear = '';
  let Notes = '';

  let AkaNames = [];
  let AKAHumanId= '';
  let AKAFirstName = '';
  let AKAMiddleName = '';
  let AKALastName = '';

  let isLoading = true;

  let FormValid = false;
  let AKAFormValid = false;
  async function setName(_FirstName, _MiddleName, _LastName, _StartYear, _EndYear, _Notes) {
    FirstName=_FirstName;
    MiddleName=_MiddleName;
    LastName=_LastName;
    StartYear=_StartYear;
    EndYear=_EndYear;
    Notes=_Notes;
  }
  $: {
    FormValid = FirstName && LastName && StartYear && EndYear && StartYear <= EndYear;
    AKAFormValid = AKAFirstName && AKALastName;
  }

  async function setAkaNames(data) {
    AkaNames = data;
  }

  onMount(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    HumanId = urlParams.get("HumanId") || "";
    if (HumanId) {
      await Promise.all([
        handleGet(HumanId, setName),
        handleGetAKA(HumanId, setAkaNames)
      ]);
    }
    console.log("HumanId", HumanId);
    isLoading = false;
  });
</script>

{#if isLoading}
  <div class="loading-screen">
    <div class="spinner"></div>
  </div>
{:else}
<div class="section">
  <a href="/Humans">Back to Humans</a>
  <div class="ActionBox">
    <h3 class="title is-2">Edit Human</h3>
  <form>
    <div class="field">
      <label class="label" for="FirstName">First Name:</label>
      <div class="control">
        <input class="input" type="text" id="FirstName" bind:value={FirstName} required>
      </div>
    </div>
    <div class="field">
      <label class="label" for="MiddleName">Middle Name:</label>
      <div class="control">
        <input class="input" type="text" id="MiddleName" bind:value={MiddleName}>
      </div>
    </div>
    <div class="field">
      <label class="label" for="LastName">Last Name:</label>
      <div class="control">
        <input class="input" type="text" id="LastName" bind:value={LastName} required>
      </div>
    </div>
    <div class="field">
      <label class="label" for="StartYear">Start Year:</label>
      <div class="control">
        <input class="input" type="number" id="StartYear" bind:value={StartYear} required>
      </div>
    </div>
    <div class="field">
      <label class="label" for="EndYear">End Year:</label>
      <div class="control">
        <input class="input" type="number" id="EndYear" bind:value={EndYear} required>
      </div>
    </div>
    <div class="field">
      <label class="label" for="Notes">Notes:</label>
      <div class="control">
        <textarea class="textarea" id="Notes" bind:value={Notes}></textarea>
      </div>
    </div>
    <div class="ActionBox">
      <label class="label" for="AkaNames">Also Known As:</label>
      {#if AkaNames.length}
        <ul>
          {#each AkaNames as akaName}
            <li>
              {akaName.AKAFirstName} {akaName.AKAMiddleName} {akaName.AKALastName}
              <button style="padding:0px;padding-left:5px;padding-right:5px;" on:click={() => handleDeleteAkaName(akaName.AKAHumanId, HumanId)}>X</button>
            </li>
          {/each}
        </ul>
      {:else}
        <p>No also known as names added yet.</p>
      {/if}
      <div class="control">
       
        <input type="hidden" id="AKAHumanId" bind:value={AKAHumanId}>
        <input class="input" type="text" id="AKAFirstName" placeholder="AKA First Name" bind:value={AKAFirstName}><br>
        <input class="input" type="text" id="AKAMiddleName" placeholder="AKA Middle Name" bind:value={AKAMiddleName}><br>
        <input class="input" type="text" id="AKALastName" placeholder="AKA Last Name" bind:value={AKALastName}><br>
        <button class="button is-primary" type="button" on:click={() => handleSaveAkaName(AKAHumanId, HumanId, AKAFirstName, AKAMiddleName, AKALastName, AKAFormValid)}>Add Also Known As</button>
      </div>
    </div>
    <div class="field">
      <div class="control">
        <button class="button is-primary" type="button" on:click={() => handleSave(HumanId, FirstName, MiddleName, LastName, StartYear, EndYear, Notes, FormValid)}>Save</button>
        {#if HumanId.length}
          <button class="button is-danger" type="button" on:click={() => handleDelete(HumanId)}>Delete</button>
        {/if}
      </div>
    </div>
  </form>
</div>
</div>
  {/if}
