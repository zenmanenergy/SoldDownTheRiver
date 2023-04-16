<!-- src/routes/Humans/+page.svelte -->
<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { handleSave } from './handleSave';
  import { handleDelete } from './handleDelete';

  let HumanId = '';
  let FirstName = '';
  let MiddleName = '';
  let LastName = '';
  let StartYear = '';
  let EndYear = '';
  let Notes = '';

  let formValid = false;

  $: {
    formValid = FirstName && LastName && StartYear && EndYear && StartYear <= EndYear;
  }

  onMount(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    HumanId = urlParams.get("HumanId") || "";
    console.log("HumanId", HumanId);
  });
</script>

<style>
  input:required:invalid {
    border: 1px solid red;
  }
  input:required:valid {
    border: 1px solid #ccc;
  }
</style>

<form>
  <div>
    <label for="FirstName">First Name:</label>
    <input type="text" id="FirstName" bind:value={FirstName} required>
  </div>
  <div>
    <label for="MiddleName">Middle Name:</label>
    <input type="text" id="MiddleName" bind:value={MiddleName}>
  </div>
  <div>
    <label for="LastName">Last Name:</label>
    <input type="text" id="LastName" bind:value={LastName} required>
  </div>
  <div>
    <label for="StartYear">Start Year:</label>
    <input type="number" id="StartYear" bind:value={StartYear} required>
  </div>
  <div>
    <label for="EndYear">End Year:</label>
    <input type="number" id="EndYear" bind:value={EndYear} required>
  </div>
  <div>
    <label for="Notes">Notes:</label>
    <textarea id="Notes" bind:value={Notes}></textarea>
  </div>
  <div>
    <button type="button" on:click={() => handleSave({ HumanId, FirstName, MiddleName, LastName, StartYear, EndYear, Notes, formValid })} >Save</button>
    {#if HumanId.length}
      <button type="button" on:click={() => handleDelete(HumanId)}>Delete</button>
    {/if}
  </div>
</form>
