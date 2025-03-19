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
	let datas = [];
	let columns = false
  
	let selectedButton = null;
	const buttons = [    
		//id is the array number
		//label is the plural label followed by the singular label in an array
	{ id: 1, label: ['Businesses', 'Business'], boxes: 1, boxnames: ["BusinessName"], arg:[""]},    
	{ id: 2, label: ['Humans', 'Human'], boxes: 3, boxnames: ["FirstName", "MiddleName", "LastName"], arg:["", "", ""]},    
	{ id: 3, label: ['Locations', 'Location'], boxes: 3,  boxnames: ["City", "State", "Country"], arg:["", "", ""]},    
	{ id: 4, label: ['Roles', 'Role'], boxes: 1,  boxnames: ["Role"], arg:[""]},    
	{ id: 5, label: ['Transactions', 'Transaction'], boxes: 2,  boxnames: ["TransactionId", "TransactionDate"], arg:["", ""]}];
	
	
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
		datas = []
		columns = false
		}
	}
	function setData(data){
		datas = data
	}
</script>
{#if isLoading}
<div class="loading-screen">
<div class="spinner"></div>
</div>
{:else}
<div class="section">

<div class="ActionBox">
<form>
<h3 class="title is-2">Select Search Field</h3>

<div class="row">
	{#each buttons.slice(0,3) as button}
	  <button class="button {selectedButton && selectedButton.id === button.id ? 'selected' : ''} {selectedButton ? 'disabled' : ''}" on:click={() => handleButton(button)}>{button.label[0]}</button>
	{/each}
  </div>
  
  <div class="row">
	{#each buttons.slice(3,6) as button}
	  <button class="button {selectedButton && selectedButton.id === button.id ? 'selected' : ''} {selectedButton ? 'disabled' : ''}" on:click={() => handleButton(button)}>{button.label[0]}</button>
	{/each}
  </div>
  



<div class="field">
	
  
	<br>
	{#if selectedButton}
    <h3>Search for {selectedButton.label[0]} by:</h3>
    {#each Array(selectedButton.boxes) as _, i}
      <div>
        <label for="textbox{i}">{selectedButton.boxnames[i]}</label>
        <input type="text" id="textbox{i}" bind:value={selectedButton.arg[i]}>
      </div>
    {/each}
  {/if}
  </div>
  {#if selectedButton}
  <button on:click={() =>{columns=true;handleSearch(Session.SessionId, selectedButton, setData)}}>Search</button>
  {#if columns}
  <table width=100%>
	<thead>
	  <tr>
		
	{#each selectedButton.boxnames as box}
		<th>{box}</th>
	{/each}
	  </tr>
	</thead>

	<tbody>
	<!-- {#each selectedButton.boxnames as box} -->
	
	  {#each datas as data}
		
		  <tr style="cursor: pointer;" on:click={window.open(`/${selectedButton.label[1]}?${selectedButton.label[1]}Id=${data[selectedButton.label[1]+'Id']}`)}>
			{#each selectedButton.boxnames as box}
				<td>{data[box]}</td>
			{/each}
		  </tr>
		
	  {/each}
	<!-- {/each} -->
	</tbody>

  </table>
  {/if}
  {/if}
</div>



 
<div class="field">
  <div class="control">
  </div>
</div>
</div>
{/if}