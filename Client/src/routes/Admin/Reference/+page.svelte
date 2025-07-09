<style>
	@import '/static/FormPages.css';
</style>
<script>
	import { onMount } from 'svelte';
	import { handleGetReference } from './handleGetReference.js';
	import { handleSaveReference } from './handleSaveReference.js';
	import { handleDeleteReference } from './handleDeleteReference.js';
	import { Session } from "../../Session.js";

	let isLoading = true;
	let isSaving = false;
	let isDeleting = false;
	let ReferenceId = '';
	let URL = '';
	let Notes = '';

	let isEdit = false;
	let errorMsg = '';
	let successMsg = '';

	function getReferenceIdFromURL() {
		const params = new URLSearchParams(window.location.search);
		return params.get("ReferenceId") || '';
	}

	onMount(async () => {
		await Session.handleSession();
		ReferenceId = getReferenceIdFromURL();
		isEdit = !!ReferenceId;
		if (isEdit) {
			const data = await handleGetReference(Session.SessionId, ReferenceId);
			if (data) {
				URL = data.URL || '';
				Notes = data.Notes || '';
			}
		}
		isLoading = false;
	});

	async function saveReference() {
		isSaving = true;
		errorMsg = '';
		successMsg = '';
		const refData = {
			ReferenceId,
			URL,
			Notes
		};
		try {
			const result = await handleSaveReference(Session.SessionId, refData);
			if (result && result.success) {
				successMsg = 'Reference saved successfully.';
				if (!ReferenceId && result.ReferenceId) {
					ReferenceId = result.ReferenceId;
					isEdit = true;
					window.history.replaceState({}, '', `/Admin/Reference?ReferenceId=${ReferenceId}`);
				}
			} else {
				errorMsg = (result && result.error) || 'Failed to save reference.';
			}
		} catch (e) {
			errorMsg = 'Error saving reference.';
		}
		isSaving = false;
	}

	async function deleteReference() {
		if (!ReferenceId) return;
		if (!confirm('Are you sure you want to delete this reference?')) return;
		isDeleting = true;
		errorMsg = '';
		successMsg = '';
		try {
			const result = await handleDeleteReference(Session.SessionId, ReferenceId);
			if (result && result.success) {
				window.location.href = '/Admin/References';
			} else {
				errorMsg = (result && result.error) || 'Failed to delete reference.';
			}
		} catch (e) {
			errorMsg = 'Error deleting reference.';
		}
		isDeleting = false;
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
			<h3 class="title is-3">{isEdit ? 'Edit Reference' : 'Add Reference'}</h3>
			{#if isEdit}
				<button class="button is-danger" type="button" on:click={deleteReference} disabled={isDeleting} style="margin-left: 1em;">
					{isDeleting ? 'Deleting...' : 'Delete'}
				</button>
			{/if}
			</div>
			{#if errorMsg}
				<div class="notification is-danger">{errorMsg}</div>
			{/if}
			{#if successMsg}
				<div class="notification is-success">{successMsg}</div>
			{/if}
			<form on:submit|preventDefault={saveReference}>
				<div class="field">
					<label class="label">URL</label>
					<div class="control">
						<input class="input" type="text" bind:value={URL} maxlength="255" required />
					</div>
				</div>
				<div class="field">
					<label class="label">Notes</label>
					<div class="control">
						<input class="input" type="text" bind:value={Notes} maxlength="255" />
					</div>
				</div>
				<div class="field">
					<div class="control">
						<button class="button is-primary" type="submit" disabled={isSaving}>
							{isSaving ? 'Saving...' : 'Save'}
						</button>
						
					</div>
				</div>
			</form>
		</div>
	</div>
{/if}
