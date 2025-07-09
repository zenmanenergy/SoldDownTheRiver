<!-- src/routes/Roles/+page.svelte -->
<style>
	@import '/static/FormPages.css';
	
</style>

<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleGetHumans } from './handleGetHumans.js';
	import { handleSaveHumanRole } from './handleSaveHumanRole.js';
	import {Session} from "../../Session.js";

	
	let Svelecte;
	let formValid = false;
	
	let isLoading = true;
	let HumanId=""
	let Role=""
	let RoleId=""
	let Humans=[]
	let Query="a"
	
	
	async function setHumans(data) {
		Humans=data
	}
	
	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		RoleId = urlParams.get("RoleId") || "";
		Role = urlParams.get("Role") || "";
		await Promise.all([
			await handleGetHumans(Session.SessionId,RoleId,Query, setHumans)
			
		]);
		
		const module = await import('svelecte');
		Svelecte = module.default || module;
		
		Promise.resolve().then(() => {
			const svelecteHuman = document.querySelector('#svelecteHuman');
			const svelecteHumanSearch = svelecteHuman.querySelector('input');
			if (svelecteHumanSearch) {
				svelecteHumanSearch.addEventListener('input', handleHumanInput);
			}

		});
		isLoading = false;
	});
	function handleHumanInput(event) {
		console.log("Input changed to:", event.target.value);
		if (event.target.value.length<=1){
			Query=event.target.value
			handleGetHumans(Session.SessionId, Role.RoleId,Query, setHumans)
		}
	}
	async function confirmDelete() {
		const userConfirmed = confirm('Are you sure you want to delete this role?\n\nWarning!!! it will delete all associations with the human records too');
		if (userConfirmed) {
			console.log("delete")
			await handleDelete(Session.SessionId, Role.RoleId);
		}
	}
	function addHuman(){
		window.location.href = '/Admin/Human/'+Role.RoleId+"/";
	}
</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner"></div>
	</div>
{:else}

	<!-- ... (previous code) -->


<!-- ... (rest of your code) -->

	<div class="section">
		<a href="/Role?RoleId={RoleId}">Back to {Role} Role</a>
		<div class="ActionBox">
			<h3 class="title is-2">Add Human to {Role}</h3>
				
			<div class="control">
				
				
				<div class="field" id="svelecteHuman">
					<svelte:component 
						this={Svelecte} 
						bind:value={HumanId} 
						on:input={handleHumanInput} 
						options={Humans.map(human => ({
							value: human.HumanId, 
							label: `${human.FirstName} ${human.LastName}`
						}))} 
					/>
				
				</div>
				<br/>
				
			
				<button class="button is-primary" on:click={()=>handleSaveHumanRole(Session.SessionId,RoleId,HumanId)}>Save Human Role</button>
				
			</div>
		</div>
	</div>
{/if}
