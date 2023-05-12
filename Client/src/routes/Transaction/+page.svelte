<!-- src/routes/Transactions/+page.svelte -->
<style>
	@import '/static/FormPages.css';
</style>
<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleSave } from './handleSave.js';
	import { handleDelete } from './handleDelete.js';
	import { handleGet } from './handleGet.js';
	import { handleGetBusinesses } from './handleGetBusinesses.js';
	import { handleGetHumans } from './handleGetHumans.js';
	import { handleGetTransactionHumans } from './handleGetTransactionHumans.js';
	import { handleSaveTransactionHuman } from './handleSaveTransactionHuman.js';
	import {Session} from "../Session.js";
	
	let LastModified='';
	let TransactionId = "";
	let TransactionDate = "";
	let FromBusinessId = "";
	let ToBusinessId = "";
	let TransactionType = "";
	let Notes = "";
	let Act = "";
	let Page = "";
	let NotaryBusinessId = "";
	let Volume = "";
	let URL = "";
	let TransactionHumanId="";
	let HumanPrice="";
	let HumanNotes="";

	let formValid = false;
	let isLoading = true;

	let Businesses=[];
	let TransactionHumans=[];
	let Humans=[];

	async function setTransactionDetails(data) {
		if (data.TransactionId){
			console.log(data)
			TransactionId = data.TransactionId;
			if (data.TransactionDate){
				TransactionDate = new Date(data.TransactionDate).toISOString().slice(0, 10); // convert to string in "YYYY-MM-DD" format
			}else{
				TransactionDate = "";
			}
			FromBusinessId = data.FromBusinessId;
			ToBusinessId = data.ToBusinessId;
			TransactionType = data.TransactionType;
			Notes = data.Notes;
			Act = data.Act;
			Page = data.Page;
			NotaryBusinessId = data.NotaryBusinessId;
			Volume = data.Volume;
			URL = data.URL;
			LastModified = data.LastModified;
			console.log("TransactionId", TransactionId)
		}
	}
	async function setBusinesses(data) {
		Businesses = data;
	}
	async function setTransactionHumans(data) {
		TransactionHumans = data;
	}
	async function setHumans(data) {
		Humans = data;
	}
	
	
	$: {
		formValid = TransactionDate && FromBusinessId && ToBusinessId;
	}
	
	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		TransactionId = urlParams.get("TransactionId") || "";
		
		
			await Promise.all([
				handleGetBusinesses(Session.SessionId,setBusinesses),
				handleGet(Session.SessionId,TransactionId, setTransactionDetails),
				handleGetTransactionHumans(Session.SessionId,TransactionId, setTransactionHumans),
				
				handleGetHumans(Session.SessionId,TransactionId, setHumans),
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
		<a href="/Transactions">Back to Transactions</a>
		<div class="ActionBox">
			<form>
				<h3 class="title is-2">Edit Transaction</h3>
	
				<input type="hidden" bind:value={TransactionId} />
	
				<div class="field">
					<label class="label" for="TransactionDate">Transaction Date</label>
					<div class="control">
						
						<input class="input" type="date" id="TransactionDate" bind:value={TransactionDate} required/>
					</div>
				</div>
	
				<div class="field">
					<label class="label" for="FromBusinessId">From:</label>
					<div class="control">
						<select class="input" id="FromBusinessId" bind:value={FromBusinessId} required>
							<option value=""></option>
							{#each Businesses as Business}
								<option value={Business.BusinessId}>{Business.BusinessName}</option>
							{/each}
						</select>
					</div>
				</div>
	
				<div class="field">
					<label class="label" for="ToBusinessId">To</label>
					<div class="control">
						<select class="input" id="ToBusinessId" bind:value={ToBusinessId} required>
							<option value=""></option>
							{#each Businesses as Business}
								<option value={Business.BusinessId}>{Business.BusinessName}</option>
							{/each}
						</select>
					</div>
				</div>
	
				<div class="field">
					<label class="label" for="TransactionType">Transaction Type</label>
					<div class="control">
						<select class="input" id="TransactionType" bind:value={TransactionType} required>
							<option value=""></option>
							<option value="Sale">Sale</option>
							<option value="Trade">Trade</option>
						</select>
					</div>
				</div>
				<div class="field">
					<label class="label" for="Notes">Notes</label>
					<div class="control">
						<textarea class="textarea" id="Notes" placeholder="Enter Notes" bind:value={Notes} required></textarea>
					</div>
				</div>
	
				<div class="field">
					<label class="label" for="Act">Act</label>
					<div class="control">
						<input class="input" type="text" id="Act" placeholder="Enter Act" bind:value={Act}/>
					</div>
				</div>
	
				<div class="field">
					<label class="label" for="Page">Page</label>
					<div class="control">
						<input class="input" type="text" id="Page" placeholder="Enter Page" bind:value={Page}/>
					</div>
				</div>
	
				<div class="field">
					<label class="label" for="NotaryBusinessId">Notary Human ID</label>
					<div class="control">
						<select class="input" id="NotaryBusinessId" bind:value={NotaryBusinessId} required>
							<option value="">Select From Human ID</option>
							{#each Businesses as Business}
								<option value={Business.BusinessId}>{Business.BusinessName}</option>
							{/each}
						</select>
					</div>
				</div>
	
				<div class="field">
					<label class="label" for="Volume">Volume</label>
					<div class="control">
						<input class="input" type="text" id="Volume" placeholder="Enter Volume" bind:value={Volume}/>
					</div>
				</div>
	
				<div class="field">
					<label class="label" for="URL">URL</label>
					<div class="control">
						<input class="input" type="url" id="URL" placeholder="Enter URL" bind:value={URL}/>
					</div>
				</div>
				<div class="field">
					<label class="label" for="Tran">Human ID</label>
					<div class="control">
						<select class="input" id="HumanId" bind:value={TransactionHumanId} required>
							<option value="">Select From Human ID</option>
							{#each Humans as Human}
								<option value={Human.HumanId}>{Human.FirstName} {Human.LastName}</option>
							{/each}
						</select>
						<br/>
						<input class="input" type="text" id="HumanPrice" placeholder="Enter Price" bind:value={HumanPrice}/>
						<br/>
						<input class="input" type="text" id="HumanNotes" placeholder="Enter Notes" bind:value={HumanNotes}/>
						<br/>
						
						<button class="button "type="button"on:click={() => handleSaveTransactionHuman(Session.SessionId,TransactionId,TransactionHumanId,HumanPrice,HumanNotes, setTransactionHumans)} >Add to Transaction</button>
					</div>
				</div>
				<div class="ActionBox">
					<h3 class="title is-2">List of Humans</h3>
					<table width=100%>
					  <thead>
						<tr>
						  <th>First Name</th>
						  <th>Last Name</th>
						  <th>Last Modified</th>
						</tr>
					  </thead>
					  <tbody>
						{#each TransactionHumans as human}
						  <tr style="cursor: pointer;" on:click={location.href=`/Human?HumanId=${human.HumanId}`}>
							<td>{human.FirstName}</td>
							<td>{human.LastName}</td>
							<td>{moment.utc(human.LastModified).local().fromNow()}</td>
						  </tr>
						{/each}
					  </tbody>
					</table>
				  </div>
	
				<div class="field">
					<div class="control">
						<button class="button is-primary" type="button" on:click={() =>   handleSave(Session.SessionId,TransactionId,TransactionDate,FromBusinessId,ToBusinessId,TransactionType,Notes,Act,Page,NotaryBusinessId,Volume,URL,formValid   ) }> Save
						</button>
						{#if TransactionId.length}
							<button class="button is-danger"type="button"on:click={() => handleDelete(Session.SessionId,TransactionId)} >Delete</button>
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