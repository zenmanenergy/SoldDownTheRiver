<!-- src/routes/Users/+page.svelte -->
<script>
	import { onMount } from 'svelte';
	import { handleSave } from './handleSave.js';
	import { handleDelete } from './handleDelete.js';
	import { handleGet } from './handleGet.js';

	let UserId="";
	let FirstName = "";
	let LastName = "";
	let Email = "";
	let Phone = "";
	let Password = "";
	let School = "";
	let SemesterYear = "";
	let formValid = false;
  	let isLoading = true;

	async function setUser(newFirstName, newLastName, newEmail, newPhone, newPassword, newSchool, newSemesterYear) {
		FirstName = newFirstName;
		LastName = newLastName;
		Email = newEmail;
		Phone = newPhone;
		Password = newPassword;
		School = newSchool;
		SemesterYear = newSemesterYear;
	}

	$: {
		formValid = FirstName && LastName && Email && Phone && Password && School && SemesterYear;
	}
	onMount(async () => {
		const urlParams = new URLSearchParams(window.location.search);
		UserId = urlParams.get("UserId") || "";
		if (UserId) {
			handleGet(UserId, setUser);
		}
		console.log("UserId", UserId)
    	isLoading = false;
	});
</script>

<style>
	input:required:invalid {
		border: 1px solid red;
	}
	input:required:valid {
		border: 1px solid #ccc;
	}
</style>

{#if isLoading}
  <div class="loading-screen">
    <div class="spinner"></div>
  </div>
{:else}
	<div>
		<form>
			<h2>Add a User</h2>

			<input type="hidden" bind:value={UserId} />

			<div>
				<label for="FirstName">First Name</label>
				<input
					type="text"
					id="FirstName"
					placeholder="Enter First Name"
					bind:value={FirstName}
					required
				/>
			</div>

			<div>
				<label for="LastName">Last Name</label>
				<input
					type="text"
					id="LastName"
					placeholder="Enter Last Name"
					bind:value={LastName}
					required
				/>
			</div>

			<div>
				<label for="Email">Email</label>
				<input
					type="email"
					id="Email"
					placeholder="Enter Email Address"
					bind:value={Email}
					required
				/>
			</div>

			<div>
				<label for="Phone">Phone</label>
				<input
					type="tel"
					id="Phone"
					placeholder="Enter Phone Number"
					bind:value={Phone}
					required
				/>
			</div>

			<div>
				<label for="Password">Password</label>
				<input
					type="password"
					id="Password"
					placeholder="Enter Password"
					bind:value={Password}
					required
				/>
			</div>

			<div>
				<label for="School">School</label>
				<input
					type="text"
					id="School"
					placeholder="Enter School Name"
					bind:value={School}
					required
				/>
			</div>

			<div>
				<label for="SemesterYear">Semester/Year</label>
				<input
					type="text"
					id="SemesterYear"
					placeholder="Enter Semester/Year"
					bind:value={SemesterYear}
					required
				
					/>
				</div>
		
				<div>
					<button type="button" on:click={() => handleSave(UserId, FirstName, LastName, Email, Phone, Password, School, SemesterYear, formValid)} >Save</button>
					{#if UserId.length}
						<button type="button" on:click={() => handleDelete(UserId)}>Delete</button>
					{/if}
				</div>
			</form>
		</div>
	{/if}