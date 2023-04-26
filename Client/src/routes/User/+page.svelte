<!-- src/routes/Users/+page.svelte -->
<style>
	@import '/static/FormPages.css';
  </style>
<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleSave } from './handleSave.js';
	import { handleDelete } from './handleDelete.js';
	import { handleGet } from './handleGet.js';
	import {Session} from "../Session.js";

	let UserId="";
	let FirstName = "";
	let LastName = "";
	let Email = "";
	let Phone = "";
	let Password = "";
	let School = "";
	let SemesterYear = "";
	let UserType=""

	let formValid = false;
  	let isLoading = true;
	

	async function setUser(_FirstName, _LastName, _Email, _Phone, _Password, _School, _SemesterYear,_UserType) {
		FirstName = _FirstName;
		LastName = _LastName;
		Email = _Email;
		Phone = _Phone;
		Password = _Password;
		School = _School;
		SemesterYear = _SemesterYear;
		UserType= _UserType
	}

	$: {
		formValid = FirstName && LastName && Email && Phone && Password && School && SemesterYear && UserType;
	}
	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		UserId = urlParams.get("UserId") || "";
		handleGet(Session.SessionId,UserId, setUser);
		
		console.log("UserId", UserId)
    	isLoading = false;
	});
</script>


{#if isLoading}
  <div class="loading-screen">
    <div class="spinner"></div>
  </div>
{:else}

  <div class="section">
	<a href="/Users">Back to Users</a>
	<div class="ActionBox">
	<form>
		<h3 class="title is-2">Add a User</h3>
		<input type="hidden" bind:value={UserId} />

		<div class="field">
			<label class="label" for="FirstName">First Name</label>
			<div class="control">
				<input
					class="input"
					type="text"
					id="FirstName"
					placeholder="Enter First Name"
					bind:value={FirstName}
					required
				/>
			</div>
		</div>

		<div class="field">
			<label class="label" for="LastName">Last Name</label>
			<div class="control">
				<input
					class="input"
					type="text"
					id="LastName"
					placeholder="Enter Last Name"
					bind:value={LastName}
					required
				/>
			</div>
		</div>

		<div class="field">
			<label class="label" for="Email">Email</label>
			<div class="control">
				<input
					class="input"
					type="email"
					id="Email"
					placeholder="Enter Email Address"
					bind:value={Email}
					required
				/>
			</div>
		</div>

		<div class="field">
			<label class="label" for="Phone">Phone</label>
			<div class="control">
				<input
					class="input"
					type="tel"
					id="Phone"
					placeholder="Enter Phone Number"
					bind:value={Phone}
					required
				/>
			</div>
		</div>

		<div class="field">
			<label class="label" for="Password">Password</label>
			<div class="control">
				<input
					class="input"
					type="password"
					id="Password"
					placeholder="Enter Password"
					bind:value={Password}
					required
				/>
			</div>
		</div>

		<div class="field">
			<label class="label" for="School">School</label>
			<div class="control">
				<input
					class="input"
					type="text"
					id="School"
					placeholder="Enter School Name"
					bind:value={School}
					required
				/>
			</div>
		</div>

		<div class="field">
			<label class="label" for="SemesterYear">Semester/Year</label>
			<div class="control">
				<input
					class="input"
					type="text"
					id="SemesterYear"
					placeholder="Enter Semester/Year"
					bind:value={SemesterYear}
					required
				/>
			</div>
		</div>
		<div class="field">
			<label class="label" for="UserType">Type</label>
			<div class="control">
				<select class="input" id="UserType" bind:value={UserType} required>
					<option value=""></option>
					<option value="Administrator">Administrator</option>
					<option value="Transcriber">Transcriber</option>
					
				  </select>
			</div>
		</div>
		<div class="field">
			<div class="control">
				<button class="button is-primary" type="button" on:click={() => handleSave(Session.SessionId,UserId, FirstName, LastName, Email, Phone, Password, School, SemesterYear,UserType, formValid)} >Save</button>
				{#if UserId.length}
					<button class="button is-danger" type="button" on:click={() => handleDelete(Session.SessionId,UserId)}>Delete</button>
				{/if}
			</div>
		</div>
		</form>
	</div>
</div>
	{/if}