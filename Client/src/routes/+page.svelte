<style>
	@import '/static/FormPages.css';
	.logout-button {
		background: none;
		border: none;
		color: blue;
		text-decoration: underline;
		cursor: pointer;
		font-size: inherit;
	}
	.logout-button:hover {
		text-decoration: none;
	}
</style>
<script>
	import { onMount } from "svelte";
	import {Session} from "./Session.js";
	import { handleLogout } from './handleLogout.js';
	
	
	let isLoading = true;
	
	onMount(async () => {
		isLoading = false;
		await Session.handleSession();
		
	});
</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner" />
	</div>
{:else}
<div class="section">
	<div class="ActionBox">
	<h3 class="title is-2">Reviewer Menu</h3>
		<ul>
			NOLA data
			<li><a href={`/Transactions`}>Transactions</a></li>
			<li><a href={`/Humans`}>Humans</a></li>
			<li><a href={`/Locations`}>Locations</a></li>
			<li><a href={`/Roles`}>Roles</a></li>
			<li><a href={`/RawNOLAs`}>Raw NOLA data</a></li>

			Manifest data (slightly outdated)
			<li><a href={`/Ships`}>Ships</a></li>
			<li><a href={`/Voyages`}>Voyages</a></li>
			<li><a href={`/Businesses`}>Businesses</a></li>
			<!-- <li><a href={`/Users`}>Users</a></li> -->
				
			
			<li>
				<button on:click={handleLogout} class="logout-button">Logout</button>
			</li>
			<br>
			
			<!-- <li><a href={`/Import`}>Import Data</a></li> -->
		</ul>
	</div>
</div>
{/if}
