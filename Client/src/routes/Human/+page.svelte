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
  import { handleGetPartners } from './handleGetPartners.js';
  import { handleDeletePartner } from './handleDeletePartner.js';
  import { handleGetPossiblePartners } from './handleGetPossiblePartners.js';
  import { handleSavePartner } from './handleSavePartner.js';
  import { handleGetRoles } from './handleGetRoles.js';
	import {Session} from "../Session.js";
  
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

  let Partners=[];

  let PartnerHumanId='';
  let PossiblePartners=[]

  let RoleId='';
  let Roles=[];

  let isLoading = true;

  let FormValid = false;
  let AKAFormValid = false;
  async function setName(_FirstName, _MiddleName, _LastName, _StartYear, _EndYear, _Notes, _RoleId) {
    FirstName=_FirstName;
    MiddleName=_MiddleName;
    LastName=_LastName;
    StartYear=_StartYear;
    EndYear=_EndYear;
    Notes=_Notes;
    RoleId=_RoleId;
    console.log(RoleId)
  }
  $: {
    FormValid = FirstName && LastName && StartYear && EndYear && StartYear <= EndYear;
    AKAFormValid = AKAFirstName && AKALastName;
  }

  async function setAkaNames(data) {
    AkaNames = data;
  }
  async function setPartners(data) {
    Partners = data;
  }
  async function setPossiblePartners(data) {
    PossiblePartners = data;
  }
  async function setRoles(data) {
    Roles = data;
  }
  onMount(async () => {
		await Session.handleSession();
    const urlParams = new URLSearchParams(window.location.search);
    HumanId = urlParams.get("HumanId") || "";
    
    await Promise.all([
      handleGet(Session.SessionId,HumanId, setName),
      handleGetAKA(Session.SessionId,HumanId, setAkaNames),
      handleGetPartners(Session.SessionId,HumanId, setPartners),
      handleGetPossiblePartners(Session.SessionId,HumanId, setPossiblePartners),
      handleGetRoles(Session.SessionId,setRoles)
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
      <label class="label" for="Role">Role:</label>
      <div class="control">
        <select id="RoleId" bind:value={RoleId}>
          <option value="">Select Role</option>
          {#each Roles as Role}
            <option value={Role.RoleId}>{Role.Role}</option>
          {/each}
        </select>
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
              <button style="padding:0px;padding-left:5px;padding-right:5px;" on:click={() => handleDeleteAkaName(Session.SessionId,akaName.AKAHumanId, HumanId)}>X</button>
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
        <button class="button is-primary" type="button" on:click={() => handleSaveAkaName(Session.SessionId,AKAHumanId, HumanId, AKAFirstName, AKAMiddleName, AKALastName, AKAFormValid)}>Add Also Known As</button>
      </div>
    </div>

    <div class="ActionBox">
      <label class="label" for="AkaNames">Partners:</label>
      {#if Partners.length}
        <ul>
          {#each Partners as partner}
            <li>
              {partner.FirstName} {partner.MiddleName} {partner.LastName}
              <button style="padding:0px;padding-left:5px;padding-right:5px;" on:click={() => handleDeletePartner(Session.SessionId,partner.PartnerHumanId, HumanId)}>X</button>
            </li>
          {/each}
        </ul>
      {:else}
        <p>No also known as names added yet.</p>
      {/if}
      <div class="control">
       
        <select id="PartnerHumanId" bind:value={PartnerHumanId}>
          <option value="">Select Partner</option>
          {#each PossiblePartners as possiblePartner}
            <option value={possiblePartner.HumanId}>{possiblePartner.FirstName} {possiblePartner.MiddleName} {possiblePartner.LastName}</option>
          {/each}
        </select>
        
        <button class="button is-primary" type="button" on:click={() => handleSavePartner(Session.SessionId,HumanId, PartnerHumanId)}>Add Partner</button>
      </div>
    </div>
    <div class="field">
      <div class="control">
        <button class="button is-primary" type="button" on:click={() => handleSave(Session.SessionId,HumanId, FirstName, MiddleName, LastName, StartYear, EndYear, Notes,RoleId, FormValid)}>Save</button>
        {#if HumanId.length}
          <button class="button is-danger" type="button" on:click={() => handleDelete(Session.SessionId,HumanId)}>Delete</button>
        {/if}
      </div>
    </div>
  </form>
</div>
</div>
  {/if}
