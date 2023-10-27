<!-- src/routes/Humans/+page.svelte -->
<style>
	@import '/static/FormPages.css';
</style>
<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { handleGetVoyageHuman} from './handleGetVoyageHuman.js';
	import { handleGetSlaveTraders} from './handleGetSlaveTraders.js';
	import { handleGetSlaveShippingAgents} from './handleGetSlaveShippingAgents.js';
	import { handleGetSlaveCollectingAgents} from './handleGetSlaveCollectingAgents.js';
	import {Session} from "../../Session.js";
	
	let Svelecte;
	let VoyageId=""
	let HumanId=""
	let VoyageHuman=[];
	let SlaveTraders=[];
	let SlaveShippingAgents=[];
	let SlaveCollectingAgents=[];
	let isLoading=true;
	
	async function setVoyageHuman(data) {
		VoyageHuman = data;
	}
	async function setSlaveTraders(data) {
		SlaveTraders = data;
	}
	async function setSlaveShippingAgents(data) {
		SlaveShippingAgents = data;
	}
	async function setSlaveCollectingAgents(data) {
		SlaveCollectingAgents = data;
	}
	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		VoyageId = urlParams.get("VoyageId") || "";
		HumanId = urlParams.get("HumanId") || "";
		await Promise.all([
			handleGetVoyageHuman(Session.SessionId,VoyageId, HumanId, setVoyageHuman),
			handleGetSlaveTraders(Session.SessionId,setSlaveTraders),
			handleGetSlaveShippingAgents(Session.SessionId,setSlaveShippingAgents),
			handleGetSlaveCollectingAgents(Session.SessionId,setSlaveCollectingAgents)
		]);
	 
		const module = await import('svelecte');
			Svelecte = module.default || module;
		isLoading = false;
	});
	
</script>
{#if isLoading}
	<div class="loading-screen">
		<div class="spinner"></div>
	</div>
{:else}
<div class="section">
	<a href="/Humans">Back to Humans</a>
	<div class="ActionBox">
		
	<form>
		<div class="field">
			<label class="label" for="FirstName">First Name:</label>
			<div class="control">
				<input class="input" type="text" id="FirstName" bind:value={VoyageHuman.FirstName} required>
			</div>
		</div>
		<div class="field">
			<label class="label" for="MiddleName">Middle Name:</label>
			<div class="control">
				<input class="input" type="text" id="MiddleName" bind:value={VoyageHuman.MiddleName}>
			</div>
		</div>
		<div class="field">
			<label class="label" for="LastName">Last Name:</label>
			<div class="control">
				<input class="input" type="text" id="LastName" bind:value={VoyageHuman.LastName} required>
			</div>
		</div>
		<div class="field">
			<label class="label" for="Size">Selling Slave Trader <a class="AddLink" href="/Human/SlaveTrader">Add Slave Trader</a></label>
						
			<div class="control">
				<div id="svelecteEndLocation">
					<Svelecte bind:value={VoyageHuman.SellingSlaveTraderHumanId} options={SlaveTraders.map(SlaveTrader => ({value: SlaveTrader.HumanId, label: SlaveTrader.FirstName+" "+SlaveTrader.LastName}))} />
					
				</div>
			</div>
		</div>
		<div class="field">
			<label class="label" for="Size">Buying Slave Trader <a class="AddLink" href="/Human/SlaveTrader">Add Slave Trader</a></label>
			<div class="control">
				<div id="svelecteEndLocation">
					<Svelecte bind:value={VoyageHuman.BuyingSlaveTraderHumanId} options={SlaveTraders.map(SlaveTrader => ({value: SlaveTrader.HumanId, label: SlaveTrader.FirstName+" "+SlaveTrader.LastName}))} />
				</div>
			</div>
		</div>
		
		<div class="field">
			<label class="label" for="Size">Shipping Agent <a class="AddLink" href="/Human/SlaveShippingAgent">Add Shipping Agent</a></label>
			<div class="control">
				<div id="svelecteEndLocation">
					<Svelecte bind:value={VoyageHuman.ShippingAgentHumanId} options={SlaveShippingAgents.map(SlaveShippingAgent => ({value: SlaveShippingAgent.HumanId, label: SlaveShippingAgent.FirstName+" "+SlaveShippingAgent.LastName}))} />
				</div>
			</div>
		</div>
		<div class="field">
			<label class="label" for="Size">Collecting Agent <a class="AddLink" href="/Human/SlaveCollectingAgent">Add Collecting Agent</a></label>
			<div class="control">
				<div id="svelecteEndLocation">
					<Svelecte bind:value={VoyageHuman.CollectingAgentHumanId} options={SlaveCollectingAgents.map(SlaveCollectingAgent => ({value: SlaveCollectingAgent.HumanId, label: SlaveCollectingAgent.FirstName+" "+SlaveCollectingAgent.LastName}))} />
					
				</div>
			</div>
		</div>
		
		<div class="field">
			<label class="label" for="Notes">Notes:</label>
			<div class="control">
				<textarea class="textarea" id="Notes" bind:value={VoyageHuman.Notes}></textarea>
			</div>
		</div>
		
	</form>
</div>
</div>
{/if}
