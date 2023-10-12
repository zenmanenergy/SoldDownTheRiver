<style>
		@import '/static/FormPages.css';
	</style>
	
	<script>
		import moment from 'moment';
		import { onMount } from 'svelte';
		import {handleGetShips} from './handleGetShips.js';
		import { Session } from "../Session.js";
	
		let Ships = [];
		let isLoading = true;
		async function setShips(data) {
			Ships = data;
		}
		onMount(async () => {
			await Session.handleSession();
			await Promise.all([
				await handleGetShips(Session.SessionId,setShips)
				
			]);
			isLoading = false;
		});
	
		function addShip() {
			window.location.href = '/Ship?ShipId=';
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
				<h3 class="title is-2">List of Ships</h3>
				<ul>
					{#each Ships as Ship}
						<li>
							<a href={`/Ship?ShipId=${Ship.ShipId}`}>
								{Ship.ShipName}
							</a>
						</li>
					{/each}
				</ul>
				<button on:click={addShip}>Add Ship</button>
			</div>
		</div>
	{/if}
	