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
	<div>
		<h1>Admin Menu</h1>
		<ul>
			<li><a href={`/Businesses`}>Businesses</a></li>
			<li><a href={`/Humans`}>Humans</a></li>
			<li><a href={`/Locations`}>Locations</a></li>
			<li><a href={`/Users`}>Users</a></li>
		</ul>
	</div>
{/if}
