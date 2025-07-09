<style>
	.table tbody tr:hover {
		background-color: #f0f0f0;
	}
	.search-box {
		margin-bottom: 20px;
	}
</style>

<script>
	import { onMount } from 'svelte';
	import {Session} from "../../Session.js";
	import { handleGetFamilies } from './handleGetFamilies.js';

	let families = [];
	let searchQuery = '';
	let error = null;

	async function fetchFamilies() {
		try {
			await handleGetFamilies((data) => {
				families = data;
				error = null;
			});
		} catch (err) {
			error = err.message;
			families = [];
		}
	}

	onMount(() => {
		fetchFamilies();
	});

	function filteredFamilies() {
		return families.filter(family =>
			family.FamilyName.toLowerCase().includes(searchQuery.toLowerCase())
		);
	}
</script>

<div class="section">
	<a href="/Admin/Humans">Back to List</a>

	<h1 class="title is-2">Families</h1>
	<div class="search-box">
		<input
			class="input"
			type="text"
			placeholder="Search families..."
			bind:value={searchQuery}
		/>
	</div>

	{#if error}
		<p style="color: red;">{error}</p>
	{/if}

	<table class="table is-fullwidth is-striped">
		<thead>
			<tr>
				<th>Family ID</th>
				<th>Family Name</th>
			</tr>
		</thead>
		<tbody>
			{#each filteredFamilies() as family}
				<tr>
					<td>{family.FamilyId}</td>
					<td>{family.FamilyName}</td>
				</tr>
			{/each}
		</tbody>
	</table>
</div>
