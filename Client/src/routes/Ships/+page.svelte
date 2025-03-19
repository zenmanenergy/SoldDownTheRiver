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
			
			<div class="ActionBox">
				<div class="title-container">
					<h3 class="title is-2">List of Ships</h3>
					<button class="button is-primary"  on:click={addShip}>Add Ship</button>
				</div>
				<ul>
					{#each Ships as Ship}
						<li>
							<a href={`/Ship?ShipId=${Ship.ShipId}`}>
								{Ship.ShipName}
							</a>
						</li>
					{/each}
				</ul>
			</div>
		</div>
	{/if}
	