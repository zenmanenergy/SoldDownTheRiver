<!-- src/routes/Businesses/+page.svelte -->
<style>
	@import '/static/FormPages.css';
  </style>
<script>
	import moment from 'moment';
	import { onMount } from 'svelte';
	import { handleLogin } from './handleLogin.js';
  
	
	let formValid = false;
	let isLoading = true;
    
    let Email="";
    let Password="";

	let invalidPassword=false
  
	$: {
	  formValid = Email && Password;
	}
  
	onMount(async () => {
	  
	  isLoading = false;
	});
  </script>
  
  
  
  {#if isLoading}
	<div class="loading-screen">
	  <div class="spinner"></div>
	</div>
  {:else}
  
	<div class="section">
		<div class="ActionBox">
	  <form>
		<h3 class="title is-2">Login</h3>
  
  
		<div class="field">
		  <label class="label" for="Email">Email</label>
		  <div class="control">
			<input
			  class="input"
			  type="email"
			  id="Email"
			  placeholder="Enter your Email"
			  bind:value={Email}
			  on:click={()=>invalidPassword = false}
			  required
			/>
		  </div>
		</div>
        <br>
		<div class="field">
            <label class="label" for="Password">Password</label>
            <div class="control">
              <input
                class="input"
                type="password"
                id="Password"
                placeholder="Enter your Password"
                bind:value={Password}
				on:click={()=>invalidPassword = false}
                required
              />
            </div>
          </div>
		<div class="field">
		  <div class="control">
			{#if invalidPassword}
				<p style="color: red;">Invalid Email or Password</p>
			{:else }
			<p style="color: white;">Enter Email and Password</p>

			{/if}

			<button class="button is-primary" type="button" on:click={() => invalidPassword = handleLogin(Email, Password,formValid)}>Login</button>
			
		  </div>
		</div>
	  </form>
	</div>
	</div>
  {/if}
  