<!-- src/routes/Businesses/+page.svelte -->
<style>
	@import '/static/FormPages.css';
  </style>
<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleSave } from './handleSave.js';
	import { handleDelete } from './handleDelete.js';
	import { handleGet } from './handleGet.js';
	import {Session} from "../Session.js";
  
	let BusinessId="";
	let BusinessName = "";
	let LastModified = "";
	let formValid = false;
	let isLoading = true;
  
	async function setName(newBusinessName, newLastModified) {
	  BusinessName = newBusinessName;
	  LastModified = newLastModified;
	}
  
	$: {
	  formValid = BusinessName;
	}
  
	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		BusinessId = urlParams.get("BusinessId") || "";
		
		handleGet(Session.SessionId,BusinessId, setName);
		
		console.log("BusinessId", BusinessId)
		isLoading = false;
	});
  </script>
  
  
  
  {#if isLoading}
	<div class="loading-screen">
	  <div class="spinner"></div>
	</div>
  {:else}
  
	<div class="section">
		<a href="/Businesses">Back to Businesses</a>
		<div class="ActionBox">
	  <form>
		<h3 class="title is-2">Add a Business</h3>
  
		<input type="hidden" bind:value={BusinessId} />
		<input type="hidden" bind:value={Session.SessionId} />
  
		<div class="field">
		  <label class="label" for="BusinessName">Name</label>
		  <div class="control">
			<input
			  class="input"
			  type="text"
			  id="BusinessName"
			  placeholder="Enter Business Name"
			  bind:value={BusinessName}
			  required
			/>
		  </div>
		</div>
  
		<div class="field">
		  <div class="control">
			<button class="button is-primary" type="button" on:click={() => handleSave(Session.SessionId, BusinessId, BusinessName,formValid)}>Save</button>
			{#if BusinessId.length}
			  <button class="button is-danger" type="button" on:click={() => handleDelete(Session.SessionId, BusinessId)}>Delete</button>
			{/if}
		  </div>
		</div>
	  </form>
		<small>Last Modified: {moment(LastModified).fromNow()}</small>
	</div>
	</div>
  {/if}
  