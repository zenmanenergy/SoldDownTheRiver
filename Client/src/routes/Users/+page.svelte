<script>
  import { onMount } from 'svelte';
  import handleGet from './handleGet.js';

  export let users = [];
  let isLoading = true;

  onMount(async () => {
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
  <div>
    <h1>List of Users</h1>
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
{/if} 
