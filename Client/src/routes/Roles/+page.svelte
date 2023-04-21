<style>
    @import '/static/FormPages.css';
  </style>
  
  <script>
    import { onMount } from 'svelte';
    import handleGet from './handleGet.js';
  
    export let roles = [];
    let isLoading = true;
  
    onMount(async () => {
      roles = await handleGet();
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
        <ul>
          {#each roles as role}
            <li>
              <a href={`/Role?RoleId=${role.RoleId}`}>{role.Role}</a>
            </li>
          {/each}
        </ul>
        <button on:click={addRole}>Add Role</button>
      </div>
    </div>
  {/if}
  