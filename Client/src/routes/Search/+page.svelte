<style>
	@import '/static/FormPages.css';
	.selected {
    background-color: #ccc;
	pointer-events: none;
  }

</style>
<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleSearch } from './handleSearch.js';
	import { Session } from "../Session.js";
  
	let selectedButton = null;
	const buttons = [    { id: 1, label: 'Business', boxes: 1, boxnames: ["BusinessName"], arg:[""]},    { id: 2, label: 'Humans', boxes: 2, boxnames: ["FirstName", "LastName"], arg:[""]},    { id: 3, label: 'Locations', boxes: 3,  boxnames: ["City", "State", "Country"], arg:[""]},    { id: 4, label: 'Roles', boxes: 1,  boxnames: ["Role"], arg:[""]},    { id: 5, label: 'Transactions', boxes: 3,  boxnames: ["TransactionId", "Business", "TransactionDate"], arg:[""]}];
	

// 
// 
// TRANSACTIONS ROLES AND HUMANS NOT WORKING??
// 
// 
// 	
	let LastModified = "";
	let formValid = false;
	let isLoading = true;
  
	// async function setName(newBusinessName, newLastModified) {
	//   BusinessName = newBusinessName;
	//   LastModified = newLastModified;
	// }
  
	// $: {
	//   formValid = BusinessName;
	// }
  
	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		// BusinessId = urlParams.get("BusinessId") || "";
		
		
		isLoading = false;
	});
	function handleButton(button) {
    if (selectedButton && selectedButton.id === button.id) {
      //change this, why didn't != work??
    } else {
      // set new selected button
      selectedButton = button;
    }
	}
	function search() {
    // Code to perform search based on selectedButton and textboxes goes here
    console.log('Searching with button', selectedButton.id);
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
<form>
<h3 class="title is-2">Select Search Field</h3>

<div class="row">
	{#each buttons.slice(0,3) as button}
	  <button class="button {selectedButton && selectedButton.id === button.id ? 'selected' : ''} {selectedButton ? 'disabled' : ''}" on:click={() => handleButton(button)}>{button.label}</button>
	{/each}
  </div>
  
  <div class="row">
	{#each buttons.slice(3,6) as button}
	  <button class="button {selectedButton && selectedButton.id === button.id ? 'selected' : ''} {selectedButton ? 'disabled' : ''}" on:click={() => handleButton(button)}>{button.label}</button>
	{/each}
  </div>
  



<div class="field">
	
  
	<br>
	{#if selectedButton}
    <h3>Search for {selectedButton.label} by:</h3>
    {#each Array(selectedButton.boxes) as _, i}
      <div>
        <label for="textbox{i}">{selectedButton.boxnames[i]}</label>
        <input type="text" id="textbox{i}" bind:value={selectedButton.arg[i]}>
      </div>
    {/each}
  {/if}
  </div>
  <button on:click={() => handleSearch(Session.SessionId, selectedButton)}>Search</button>
 </div>

<div class="field">
  <div class="control">
  </div>
</div>
</div>
{/if}