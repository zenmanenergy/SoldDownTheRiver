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
			<li><a href={`/AdminMenu`}>AdminMenu</a></li>
		</ul>
	</div>
{/if}
