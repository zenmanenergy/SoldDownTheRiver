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
	import { handleGetFromHumans } from './handleGetFromHumans.js';
	import { handleGetToHumans } from './handleGetToHumans.js';
	import { handleGetNotaryHumans } from './handleGetNotaryHumans.js';
	import {Session} from "../Session.js";
  
  let LastModified='';
	let TransactionId = "";
	let TransactionDate = "";
	let FromHumanId = "";
	let ToHumanId = "";
	let TransactionType = "";
	let Notes = "";
	let Act = "";
	let Page = "";
	let NotaryHumanId = "";
	let Volume = "";
	let URL = "";
  
	let formValid = false;
	let isLoading = true;

  let FromHumans = [];
  let ToHumans = [];
  let NotaryHumans= [];
  
	async function setTransactionDetails(data) {
      if (data.TransactionId){
        TransactionId = data.TransactionId;
        if (data.TransactionDate){
          TransactionDate = new Date(data.TransactionDate).toISOString().slice(0, 10); // convert to string in "YYYY-MM-DD" format
        }else{
          TransactionDate = "";
        }
        FromHumanId = data.FromHumanId;
        ToHumanId = data.ToHumanId;
        TransactionType = data.TransactionType;
        Notes = data.Notes;
        Act = data.Act;
        Page = data.Page;
        NotaryHumanId = data.NotaryHumanId;
        Volume = data.Volume;
        URL = data.URL;
        LastModified = data.LastModified;
        console.log("TransactionId", TransactionId)
      }
	}
  function setFromHumans(_fromHumans) {
    FromHumans = _fromHumans;
  }
  function setToHumans(_toHumans) {
    ToHumans = _toHumans;
  }
  function setNotaryHumans(_notaryHumans) {
    NotaryHumans= _notaryHumans
  }
  
	$: {
	  formValid = TransactionDate && FromHumanId && ToHumanId && TransactionType && Notes;
	}
  
	onMount(async () => {
		await Session.handleSession();
		const urlParams = new URLSearchParams(window.location.search);
		TransactionId = urlParams.get("TransactionId") || "";
    
		
			await Promise.all([
        handleGetFromHumans(Session.SessionId,TransactionId, setFromHumans),
        handleGetToHumans(Session.SessionId,TransactionId, setToHumans),
        handleGetNotaryHumans(Session.SessionId,TransactionId, setNotaryHumans),
        handleGet(Session.SessionId,TransactionId, setTransactionDetails)
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
						<input
							class="input"
							type="date"
							id="TransactionDate"
							bind:value={TransactionDate}
							required
						/>
					</div>
				</div>
  
				<div class="field">
					<label class="label" for="FromHumanId">From Human ID</label>
					<div class="control">
						<select class="input" id="FromHumanId" bind:value={FromHumanId} required>
              <option value="">Select From Human ID</option>
              {#each FromHumans as FromHuman}
                <option value={FromHuman.HumanId}>{FromHuman.FirstName} {FromHuman.LastName}</option>
              {/each}
            </select>
					</div>
				</div>
  
				<div class="field">
					<label class="label" for="ToHumanId">To Human ID</label>
					<div class="control">
						<select class="input" id="ToHumanId" bind:value={ToHumanId} required>
              <option value="">Select To Human ID</option>
              {#each ToHumans as ToHuman}
                <option value={ToHuman.HumanId}>{ToHuman.FirstName} {ToHuman.LastName}</option>
              {/each}
            </select>
					</div>
				</div>
  
				<div class="field">
					<label class="label" for="TransactionType">Transaction Type</label>
          <div class="control">
            <input
                       class="input"
                       type="text"
                       id="TransactionType"
                       placeholder="Enter Transaction Type"
                       bind:value={TransactionType}
                       required
                     />
          </div>
        </div>
        <div class="field">
          <label class="label" for="Notes">Notes</label>
          <div class="control">
            <textarea
              class="textarea"
              id="Notes"
              placeholder="Enter Notes"
              bind:value={Notes}
              required
            ></textarea>
          </div>
        </div>
  
        <div class="field">
          <label class="label" for="Act">Act</label>
          <div class="control">
            <input
              class="input"
              type="text"
              id="Act"
              placeholder="Enter Act"
              bind:value={Act}
            />
          </div>
        </div>
  
        <div class="field">
          <label class="label" for="Page">Page</label>
          <div class="control">
            <input
              class="input"
              type="text"
              id="Page"
              placeholder="Enter Page"
              bind:value={Page}
            />
          </div>
        </div>
  
        <div class="field">
          <label class="label" for="NotaryHumanId">Notary Human ID</label>
          <div class="control">
            <select class="input" id="NotaryHumanId" bind:value={NotaryHumanId} required>
              <option value="">Select From Human ID</option>
              {#each NotaryHumans as NotaryHuman}
                <option value={NotaryHuman.HumanId}>{NotaryHuman.FirstName} {NotaryHuman.LastName}</option>
              {/each}
            </select>
          </div>
        </div>
  
        <div class="field">
          <label class="label" for="Volume">Volume</label>
          <div class="control">
            <input
              class="input"
              type="text"
              id="Volume"
              placeholder="Enter Volume"
              bind:value={Volume}
            />
          </div>
        </div>
  
        <div class="field">
          <label class="label" for="URL">URL</label>
          <div class="control">
            <input
              class="input"
              type="url"
              id="URL"
              placeholder="Enter URL"
              bind:value={URL}
            />
          </div>
        </div>
  
        <div class="field">
          <div class="control">
            <button
              class="button is-primary"
              type="button"
              on:click={() =>
                handleSave(Session.SessionId,
                  TransactionId,
                  TransactionDate,
                  FromHumanId,
                  ToHumanId,
                  TransactionType,
                  Notes,
                  Act,
                  Page,
                  NotaryHumanId,
                  Volume,
                  URL,
                  formValid
                )
              }
            >
              Save
            </button>
            {#if TransactionId.length}
              <button
                class="button is-danger"
                type="button"
                on:click={() => handleDelete(Session.SessionId,TransactionId)}
              >
                Delete
              </button>
            {/if}
          </div>
        </div>
      </form>
      <small>Last Modified: {moment(LastModified).fromNow()}</small>
    </div>
  </div>
  
  {/if}