<style>
  @import '/static/FormPages.css';
</style>
<script>
  import { onMount } from 'svelte';
  import handleGet from './handleGet.js';
	import {Session} from "../Session.js";

  export let users = [];
  let isLoading = true;

  onMount(async () => {
		await Session.handleSession();
    users = await handleGet();
    isLoading = false;
  });

  function addUser() {
    window.location.href = '/User?UserId=';
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
		<h3 class="title is-2">List of Users</h3>
    <ul>
      {#each users as user}
        <li>
          <a href={`/User?UserId=${user.UserId}`}>
            {user.FirstName} {user.LastName}
          </a>
        </li>
      {/each}
    </ul>
    <button on:click={addUser}>Add User</button>
  </div>
</div>
{/if} 
