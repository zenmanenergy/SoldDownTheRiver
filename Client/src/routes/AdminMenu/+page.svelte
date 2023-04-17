<style>
	@import '/static/FormPages.css';
  </style>
  <script>
	import { onMount } from "svelte";

	let isLoading = true;

	onMount(async () => {
		isLoading = false;
	});
</script>

{#if isLoading}
	<div class="loading-screen">
		<div class="spinner" />
	</div>
{:else}
<div class="section">
    <div class="ActionBox">
      <h3 class="title is-2">Admin Menu</h3>
		<ul>
			<li><a href={`/Businesses`}>Businesses</a></li>
			<li><a href={`/Humans`}>Humans</a></li>
			<li><a href={`/Locations`}>Locations</a></li>
			<li><a href={`/Users`}>Users</a></li>
		</ul>
	</div>
</div>
{/if}
