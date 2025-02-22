<!-- src/routes/Businesses/+page.svelte -->
<style>
	@import '/static/FormPages.css';
  </style>
<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import {Session} from "../Session.js";
    import { handleImport } from "./handleImport.js";
  
	
	let formValid = false;
	let isLoading = true;
    
	let SpreadsheetName="";
    let SpreadsheetData="";

	let invalidPassword=false
  
	$: {
	  formValid = SpreadsheetData;
	}
  
	onMount(async () => {
		await Session.handleSession();
	  
	  isLoading = false;
	});
  </script>
  
  
  
  {#if isLoading}
	<div class="loading-screen">
	  <div class="spinner"></div>
	</div>
  {:else}
	
  	
	<div class="section">
		<a href="/">Back to Menu</a>
		<div class="ActionBox">
			
	  <form>
		<h3 class="title is-2">Import data into the database</h3>
  
		<div class="field">
			<label class="label" for="Email">File Name</label>
			<div class="control">
				<input class="input" type="text" id="SpreadsheetName" placeholder="Enter File Name" bind:value={SpreadsheetName}><br>
			</div>
		  </div>
		<div class="field">
		  <label class="label" for="Email">SpreadSheet data</label>
		  <div class="control">
			<textarea bind:value={SpreadsheetData} class="textarea" cols="60" rows="10" placeholder="Enter Spreadsheet data"></textarea>
		  </div>
		</div>
        <br>
		
		<div class="field">
		  <div class="control">
			

			<button class="button is-primary" type="button" on:click={() => handleImport(Session.SessionId,SpreadsheetName,SpreadsheetData)}>Import</button>
			
		  </div>
		</div>
	  </form>
	</div>
	</div>
  {/if}
  