<script>
	import { onMount } from 'svelte';
	import {Session} from "../Session.js";
	import { handleGetHumans } from './handleGetHumans.js';
	
	let isLoading = true;
	let Humans = [];
	let Svelecte;
	let HumanId;
	let Query="James"
	onMount(async () => {
		const module = await import('svelecte');
		Svelecte = module.default || module;
	});
	async function setHumans(data) {
		Humans = data;
	}
	onMount(async () => {
		await Session.handleSession();
		await Promise.all([
			await handleGetHumans(Session.SessionId, Query ,setHumans)
				
		]);
		isLoading = false;
	});
	

</script>

{#if Svelecte}
<div class="section">
	<a href="/AdminMenu">Back to Menu</a>
	<div class="ActionBox">
	<Svelecte bind:value={HumanId} options={Humans.map(human => ({value: human.HumanId, label: human.FirstName+" "+human.LastName}))} />
	</div>
</div>
{/if}