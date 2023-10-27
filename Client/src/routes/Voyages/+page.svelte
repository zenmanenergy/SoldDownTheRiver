<style>
		@import '/static/FormPages.css';
	</style>
	
	<script>
		import moment from 'moment';
		import { onMount } from 'svelte';
		import {handleGetVoyages} from './handleGetVoyages.js';
		import { Session } from "../Session.js";
	
		export let Voyages = [];
		let isLoading = true;
		async function setVoyages(data) {
			Voyages = data;
		} 
	
		onMount(async () => {
			await Session.handleSession();
			await Promise.all([
				handleGetVoyages(Session.SessionId, setVoyages),

			]);
			isLoading = false;
		});
	
		function addVoyage() {
			window.location.href = '/Voyage?VoyageId=';
		}
	</script>
	
	<div class="section">
		{#if isLoading}
			<div class="loading-screen">
				<div class="spinner"></div>
			</div>
		{:else}
			<a href="/AdminMenu">Back to Menu</a>
			<div class="ActionBox">
				<div class="title-container">
					<h3 class="title is-2">List of Voyages</h3>
					<button class="button is-primary"   on:click={addVoyage}>Add Voyage</button>
				</div>
				<table class="ClickableTable" width=100%>
					<thead>
						<tr>
							<th>Ship</th>
							<th>From</th>
							<th>To</th>
						</tr>
					</thead>
					<tbody>
						{#each Voyages as Voyage}
							<tr on:click={() => window.location.href = `/Voyage?VoyageId=${Voyage.VoyageId}`}>
								<td>{Voyage.ShipName}</td>
								<td>{Voyage.StartCity} {Voyage.StartState} {moment(Voyage.StartDate).format('MMMM D, YYYY')}</td>
								<td>{Voyage.EndCity} {Voyage.EndState} {moment(Voyage.EndDate).format('MMMM D, YYYY')}</td>
							</tr>
						{/each}

						
					</tbody>
				</table>
			</div>
		{/if}
	</div>
	