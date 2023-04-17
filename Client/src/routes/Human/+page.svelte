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

  let HumanId = '';
  let FirstName = '';
  let MiddleName = '';
  let LastName = '';
  let StartYear = '';
  let EndYear = '';
  let Notes = '';
  let isLoading = true;

  let FormValid = false;
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
  }

  onMount(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    HumanId = urlParams.get("HumanId") || "";
    if (HumanId) {
      handleGet(HumanId, setName);
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