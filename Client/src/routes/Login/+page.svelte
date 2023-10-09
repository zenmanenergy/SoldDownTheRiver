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

	let validPassword=true
  
	$: {
	  formValid = Email && Password;
	}
  
	onMount(async () => {
	  
	  isLoading = false;
	});

	function loggedIn(formValid){

		validPassword = formValid
	}


	function doLogin(){

		handleLogin(Email, Password,formValid, loggedIn)
		
	}



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
			  on:click={()=>validPassword = true}
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
				on:click={()=> validPassword = true}
                required
              />
            </div>
          </div>
		<div class="field">
		  <div class="control">
			<button class="button is-primary" type="button" on:click={doLogin}>Login</button>
			
			{#if validPassword}
			<p style="color: white;">Enter Email and Password</p>

			{:else }
			<p style="color: red;">Invalid Email or Password</p>


			{/if}

		  </div>
		</div>
	  </form>
	</div>
	</div>
  {/if}
  