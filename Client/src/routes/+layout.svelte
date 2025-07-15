<!-- src/routes/+layout.svelte -->
<script>
	import Navigation from '../components/Navigation.svelte';
</script>

<Navigation />

<div id="bodycontents" style="display: block">
	<slot />
</div>

<footer class="footer">
	<div class="content has-text-centered">
		<p>
			Copyright 2025, Sold Down River Project. All rights reserved.
		</p>
	</div>
</footer>

<style>
	/* Move navigation-specific styles here if needed */
	:global(.navbar-burger) {
		background: none;
		border: none;
		cursor: pointer;
		color: white;
	}
	
	:global(.navbar-burger:hover) {
		background-color: rgba(0, 0, 0, 0.1);
	}
</style>
