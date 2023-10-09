<style>
	@import '/static/FormPages.css';
</style>
<script>
		import moment from 'moment';
		import { onMount } from 'svelte';
		import {Session} from "../Session.js";
		import { handleGetHumans } from './handleGetHumans.js';
	
		let Humans = [];
		let filteredHumans = [];
		let isLoading = true;
		let searchQuery = '';

		let currentPage = 1;
		let itemsPerPage = 50;
		let totalPages = 1;
		
		async function setHumans(data) {
			Humans = data;
		}
		onMount(async () => {
			await Session.handleSession();
			await Promise.all([
				await handleGetHumans(Session.SessionId, setHumans)
					
			]);
			isLoading = false;
		});
		

		$: filteredHumans = Humans.filter(human => {
			const fullName = `${human.FirstName} ${human.LastName}`.toLowerCase();
			return fullName.includes(searchQuery.toLowerCase());
		});
		$: totalPages = Math.ceil(filteredHumans.length / itemsPerPage);
		$: displayedHumans = filteredHumans.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);


		function addHuman() {
			window.location.href = '/Human?HumanId=';
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
				<h3 class="title is-2">List of Humans</h3>
				<form>
				<div class="field">
					<div class="control">
						<input class="input" type="text" bind:value={searchQuery} placeholder="Search by name" />
					</div>
				
					</div>
				</form>
				<table width=100%>
					<thead>
						<tr>
							<th>First Name</th>
							<th>Last Name</th>
							<th>Last Modified</th>
						</tr>
					</thead>
					<tbody>
						{#each displayedHumans as human}
							<tr style="cursor: pointer;" on:click={() => location.href=`/Human?HumanId=${human.HumanId}`}>
								<td>{human.FirstName}</td>
								<td>{human.LastName}</td>
								<td>{moment.utc(human.LastModified).local().fromNow()}</td>
							</tr>
						{/each}
						
					</tbody>
				</table>
				<div class="pagination">
					<button on:click={() => currentPage = Math.max(currentPage - 1, 1)} disabled={currentPage === 1}>
						Previous
					</button>
					<span>{currentPage} / {totalPages}</span>
					<button on:click={() => currentPage = Math.min(currentPage + 1, totalPages)} disabled={currentPage === totalPages}>
						Next
					</button>
				</div>
				<button on:click={addHuman}>Add Human</button>
			</div>
		</div>
	
	{/if}