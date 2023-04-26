<style>
    @import '/static/FormPages.css';
  </style>
  
  <script>
    import moment from 'moment';
    import { onMount } from 'svelte';
    import handleGet from './handleGet.js';
	  import {Session} from "../Session.js";
  
    export let roles = [];
    let isLoading = true;
  
    onMount(async () => {
		  await Session.handleSession();
      roles = await handleGet(Session.SessionId);
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
          {#each roles as role}
            <tr style="cursor: pointer;" on:click={location.href=`/Role?RoleId=${role.RoleId}`}>
              <td>{role.Role}</td>
              <td>{moment(role.LastModified).fromNow()}</td>
            </tr>
          {/each}
        </tbody>
      </table>
      <button on:click={addRole}>Add Role</button>
    </div>
  </div>
  
  {/if}
  