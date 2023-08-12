<style>
@import '/static/FormPages.css';
</style>
	
<script>
import moment from 'moment';
import { onMount } from 'svelte';
import {handleGetRoles} from './handleGetRoles.js';
	import {Session} from "../Session.js";

export let Roles = [];
let isLoading = true;
async function setRoles(data) {
	
	Roles=data;
}
onMount(async () => {
		await Session.handleSession();
	await Promise.all([
	await handleGetRoles(Session.SessionId,setRoles)
	]);
	isLoading = false;
});

function addRole() {
	window.location.href = '/Role?RoleId=';
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
			<h3 class="title is-2">List of Roles</h3>
			<table width=100%>
			<thead>
				<tr>
				<th>Role</th>
				<th>Last Modified</th>
				</tr>
			</thead>
			<tbody>
				{#each Roles as role}
				<tr style="cursor: pointer;" on:click={location.href=`/Role?RoleId=${role.RoleId}`}>
					<td>{role.Role}</td>
					<td>{moment.utc(role.LastModified).local().fromNow()}</td>
				</tr>
				{/each}
			</tbody>
			</table>
			<button on:click={addRole}>Add Role</button>
		</div>
	</div>
	
{/if}
