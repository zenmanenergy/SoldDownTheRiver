<!-- src/routes/Humans/+page.svelte -->
<style>
	@import '/static/FormPages.css';
</style>
<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { handleSave } from './handleSave.js';
	import { handleDelete } from './handleDelete.js';
	import { handleGetHuman } from './handleGetHuman.js';
	import { handleGetAKA } from './handleGetAKA.js';
	import { handleSaveAkaName } from './handleSaveAkaName.js';
	import { handleDeleteAkaName } from './handleDeleteAkaName.js';
	import { handleGetFamilies } from './handleGetFamilies.js';
	import { handleDeleteFamily } from './handleDeleteFamily.js';
	import { handleGetPossibleFamilies } from './handleGetPossibleFamilies.js';
	import { handleSaveFamily } from './handleSaveFamily.js';
	import { handleGetRoles } from './handleGetRoles.js';
	import {Session} from "../Session.js";
	
	let Relationship = '';
	let LastModified='';
	let HumanId = '';
	let FirstName = '';
	let MiddleName = '';
	let LastName = '';
	let StartYear = '';
	let EndYear = '';
	let Notes = '';

	let AkaNames = [];
	let AKAHumanId= '';
	let AKAFirstName = '';
	let AKAMiddleName = '';
	let AKALastName = '';

	let Families=[];

	let FamilyHumanId='';
	let PossibleFamilies=[]

	let RoleId='';
	let Roles=[];

	let isLoading = true;

	let FormValid = false;
	let AKAFormValid = false;
	async function setName(data) {
		FirstName=data._FirstName;
		MiddleName=data._MiddleName;
		LastName=data._LastName;
		StartYear=data._StartYear;
		EndYear=data._EndYear;
		Notes=data._Notes;
		RoleId=data._RoleId;
		LastModified=data._LastModified;
		
	}
	$: {
		FormValid = FirstName && LastName;
		AKAFormValid = AKAFirstName && AKALastName;
	}

	async function setAkaNames(data) {
		AkaNames = data;
	}
	async function setFamilies(data) {
		Families = data;
	}
	async function setPossibleFamilies(data) {
		PossibleFamilies = data;
	}
	async function setRoles(data) {
		Roles = data;
	}
	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		HumanId = urlParams.get("HumanId") || "";
		
		await Promise.all([
			handleGetHuman(Session.SessionId,HumanId, setName),
			handleGetAKA(Session.SessionId,HumanId, setAkaNames),
			handleGetFamilies(Session.SessionId,HumanId, setFamilies),
			handleGetPossibleFamilies(Session.SessionId,HumanId, setPossibleFamilies),
			handleGetRoles(Session.SessionId,setRoles)
		]);
	 
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
		<h3 class="title is-2">Edit Human</h3>
	<form>
		<div class="field">
			<label class="label" for="FirstName">First Name:</label>
			<div class="control">
				<input class="input" type="text" id="FirstName" bind:value={FirstName} required>
			</div>
		</div>
		<div class="field">
			<label class="label" for="MiddleName">Middle Name:</label>
			<div class="control">
				<input class="input" type="text" id="MiddleName" bind:value={MiddleName}>
			</div>
		</div>
		<div class="field">
			<label class="label" for="LastName">Last Name:</label>
			<div class="control">
				<input class="input" type="text" id="LastName" bind:value={LastName} required>
			</div>
		</div>
		<div class="field">
			<label class="label" for="Role">Role:</label>
			<div class="control">
				<select id="RoleId" bind:value={RoleId}>
					<option value="">Select Role</option>
					{#each Roles as Role}
						<option value={Role.RoleId}>{Role.Role}</option>
					{/each}
				</select>
			</div>
		</div>
		
		<div class="field">
			<label class="label" for="Notes">Notes:</label>
			<div class="control">
				<textarea class="textarea" id="Notes" bind:value={Notes}></textarea>
			</div>
		</div>
		<div class="ActionBox">
			<label class="label" for="AkaNames">Also Known As:</label>
			{#if AkaNames.length}
				<ul>
					{#each AkaNames as akaName}
						<li>
							{akaName.AKAFirstName} {akaName.AKAMiddleName} {akaName.AKALastName}
							<button style="padding:0px;padding-left:5px;padding-right:5px;" on:click={() => handleDeleteAkaName(Session.SessionId,akaName.AKAHumanId, HumanId)}>X</button>
						</li>
					{/each}
				</ul>
			{:else}
				<p>No also known as names added yet.</p>
			{/if}
			<div class="control">
			 
				<input type="hidden" id="AKAHumanId" bind:value={AKAHumanId}>
				<input class="input" type="text" id="AKAFirstName" placeholder="AKA First Name" bind:value={AKAFirstName}><br>
				<input class="input" type="text" id="AKAMiddleName" placeholder="AKA Middle Name" bind:value={AKAMiddleName}><br>
				<input class="input" type="text" id="AKALastName" placeholder="AKA Last Name" bind:value={AKALastName}><br>
				<button class="button is-primary" type="button" on:click={() => handleSaveAkaName(Session.SessionId,AKAHumanId, HumanId, AKAFirstName, AKAMiddleName, AKALastName, AKAFormValid)}>Add Also Known As</button>
			</div>
		</div>

		<div class="ActionBox">
			<label class="label" for="AkaNames">Families:</label>
			{#if Families.length}
				<ul>
					{#each Families as Family}
						<li>
							{Family.FirstName} {Family.MiddleName} {Family.LastName} {Family.Relationship}
							<button style="padding:0px;padding-left:5px;padding-right:5px;" on:click={() => handleDeleteFamily(Session.SessionId,Family.FamilyHumanId, HumanId)}>X</button>
						</li>
					{/each}
				</ul>
			{:else}
				<p>No also known as names added yet.</p>
			{/if}
			<div class="control">
			 
				<select id="FamilyHumanId" bind:value={FamilyHumanId}>
					<option value="">Select Family</option>
					{#each PossibleFamilies as possibleFamily}
						<option value={possibleFamily.HumanId}>{possibleFamily.FirstName} {possibleFamily.MiddleName} {possibleFamily.LastName}</option>
					{/each}
				</select>
				<select id="Relationship" bind:value={Relationship}>
					<option>Father</option>
					<option>Mother</option>
					<option>Sister</option>
					<option>Brother</option>
					<option>Son</option>
					<option>Daughter</option>
					<option>Unknown</option>
				</select>
				<button class="button is-primary" type="button" on:click={() => handleSaveFamily(Session.SessionId,HumanId, FamilyHumanId, Relationship)}>Add Family</button>
			</div>
		</div>
		<div class="field">
			<div class="control">
				<button class="button is-primary" type="button" on:click={() => handleSave(Session.SessionId,HumanId, FirstName, MiddleName, LastName, Notes,RoleId, FormValid)}>Save</button>
				{#if HumanId.length}
					<button class="button is-danger" type="button" on:click={() => handleDelete(Session.SessionId,HumanId)}>Delete</button>
				{/if}
			</div>
		</div>
	</form>
	{#if LastModified}
		<small>Last Modified: {moment.utc(LastModified).local().fromNow()}</small>
	{/if}
</div>
</div>
	{/if}
