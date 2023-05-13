<style>
	@import '/static/FormPages.css';
  </style>
<script>
	import { onMount } from "svelte";
	import {Session} from "../Session.js";
	
	
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
      <h3 class="title is-2">Admin Menu</h3>
		<ul>
			<li><a href={`/Businesses`}>Businesses</a></li>
			<li><a href={`/Humans`}>Humans</a></li>
			<li><a href={`/Locations`}>Locations</a></li>
			<li><a href={`/Roles`}>Roles</a></li>
			<li><a href={`/Transactions`}>Transactions</a></li>
			<li><a href={`/Ships`}>Ships</a></li><br>
			<li><a href={`/Users`}>Users</a></li><br>
				
			<li><a href={`/Search`}>Search</a></li>
		</ul>
	</div>
</div>
{/if}
