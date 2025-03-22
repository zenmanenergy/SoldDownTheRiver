<script>
	import { onMount } from 'svelte';
	import { Session } from '../Session.js';
	import { handleGetFamily } from './handleGetFamily.js';
	import { handleGetHumans } from '../Humans/handleGetHumans.js';
	import { handleAddFamilyMember } from './handleAddFamilyMember.js';

	let humanId = ''; // Input for the HumanId to fetch the tree
	let error = null;

	let HumanId = null;
	let families = [];
	let Humans = [];
	let filteredHumans = [];
	let searchQuery = '';
	let selectedHumanId = null;
	let relationshipType = '';
	let relationshipOptions = ['Husband', 'Wife', 'Son', 'Daughter', 'Father', 'Mother', 'Brother', 'Sister'];
	let isLoading = true;
	let selectedHuman = null;
	let selectedHumanData = null;
	let sortColumn = 'LastName';
	let sortAscending = true;

	// Function to generate a family tree diagram with proper hierarchy
	function generateFamilyTreeHTML(families) {
		if (!families || families.length === 0) return '<p>No family relationships available.</p>';

		// Sort families by left_value to ensure proper hierarchy
		families.sort((a, b) => a.left_value - b.left_value);

		// Recursive function to build the tree structure
		function buildTree(families, parentLeftValue = null) {
			return families
				.filter(family => {
					// A parent is identified by its left_value being less than the child's left_value
					return parentLeftValue === null || (family.left_value > parentLeftValue && family.right_value < parentLeftValue + 2);
				})
				.map(family => `
					<div class="tree-node">
						<div class="tree-box">
							${family.FirstName} ${family.LastName || ''}
							${family.SpouseFirstName || family.SpouseLastName ? `<br>(Spouse: ${family.SpouseFirstName} ${family.SpouseLastName})` : ''}
						</div>
						<div class="tree-children">
							${buildTree(families, family.left_value).join('')}
						</div>
					</div>
				`);
		}

		return `<div class="tree-root">${buildTree(families).join('')}</div>`;
	}

	$: familyTreeHTML = generateFamilyTreeHTML(families);

	// Utility function to get a URL parameter by name
	function getURLVariable(name) {
		return new URLSearchParams(window.location.search).get(name);
	}

	function setFamilies(data) {
		families = data;
		console.log(families)
	}

	

	function setHumans(data) {
		Humans = data;

		// Update selectedHumanData after fetching humans
		selectedHumanData = Humans.find(human => human.HumanId === HumanId) || null;
	}
	onMount(async () => {
		await Session.handleSession();
		HumanId = getURLVariable('HumanId') || null;

		if (HumanId) {
			await handleGetFamily(Session.SessionId, HumanId, setFamilies);
		}

		await handleGetHumans(Session.SessionId, setHumans);

		// Extract the human data from the Humans array
		selectedHumanData = Humans.find(human => human.HumanId === HumanId) || null;

		isLoading = false;
	});
	$: {
		filteredHumans = Humans.filter(human => {
			const search = searchQuery.toLowerCase();
			const values = [
				human.FirstName,
				human.MiddleName,
				human.LastName,
				formatBirthDate(human.BirthDate, human.BirthDateAccuracy),
				human.RacialDescriptor,
				human.Sex,
				human.Height_in ? human.Height_in.toString() : '',
				human.Roles ? human.Roles.join(', ') : '',
				human.HumanId // Include HumanId in the search
			];
			return values.some(value => value && value.toLowerCase().includes(search));
		});

		// Sort the filtered humans
		filteredHumans.sort((a, b) => {
			let valueA = a[sortColumn] ?? '';
			let valueB = b[sortColumn] ?? '';

			// Handle birth date sorting separately
			if (sortColumn === 'BirthDate') {
				valueA = a.BirthDate ? new Date(a.BirthDate) : new Date(0);
				valueB = b.BirthDate ? new Date(b.BirthDate) : new Date(0);
			}

			// Convert to lowercase for case-insensitive sorting
			if (typeof valueA === 'string') valueA = valueA.toLowerCase();
			if (typeof valueB === 'string') valueB = valueB.toLowerCase();

			if (valueA < valueB) return sortAscending ? -1 : 1;
			if (valueA > valueB) return sortAscending ? 1 : -1;
			return 0;
		});
	}

	function toggleSort(column) {
		if (sortColumn === column) {
			sortAscending = !sortAscending;
		} else {
			sortColumn = column;
			sortAscending = true;
		}
	}

	function selectHuman(human) {
		selectedHuman = human;
	}

	async function submitRelationship() {
		if (!selectedHuman || !relationshipType) {
			alert('Please select a human and a relationship type.');
			return;
		}

		const success = await handleAddFamilyMember(Session.SessionId, HumanId, selectedHuman.HumanId, relationshipType); // Updated function call

		if (success) {
			alert('Relationship added successfully!');
			window.location.reload();
		} else {
			alert('Failed to add relationship.');
		}
	}

	function formatBirthDate(date) {
		if (!date) return 'Unknown';
		try {
			// Convert the date string into a Date object
			const dateObj = new Date(date);
			if (isNaN(dateObj)) return 'Unknown'; // Ensure the date is valid

			// Extract the components
			const day = dateObj.getUTCDate();
			const month = dateObj.getUTCMonth() + 1; // Months are zero-based
			const year = dateObj.getUTCFullYear();

			// Format as m/d/yyyy
			return `${month}/${day}/${year}`;
		} catch (error) {
			console.error('Error formatting date:', error);
			return 'Unknown';
		}
	}
</script>



{#if isLoading}
	<div class="loading-screen">
		<div class="spinner"></div>
	</div>
{:else}
	<div class="section">
		<!-- Display Human Information -->
		{#if selectedHumanData}
			<div class="box">
				<h3 class="title is-3">Human Information</h3>
				<p><strong>Name:</strong> {selectedHumanData.FirstName} {selectedHumanData.LastName}</p>
				<p><strong>Birth Date:</strong> {formatBirthDate(selectedHumanData.BirthDate)}</p>
				<p><strong>Racial Descriptor:</strong> {selectedHumanData.RacialDescriptor || 'Unknown'}</p>
				<p><strong>Sex:</strong> {selectedHumanData.Sex || 'Unknown'}</p>
				<p><strong>Roles:</strong> {selectedHumanData.Roles.length > 0 ? selectedHumanData.Roles.join(', ') : 'No Roles'}</p>
			</div>
		{/if}

		<!-- Family Relationships Tree -->
		<div class="tree-container">
			<h3 class="title is-3">Family Tree</h3>
			{@html familyTreeHTML}
			
			<!-- Selected Human -->
			{#if selectedHuman}
			<hr>
				<div class="selected-human">
					<h4 class="title is-4">Selected Human</h4>
					<p><strong>Name:</strong> {selectedHuman.FirstName} {selectedHuman.MiddleName} {selectedHuman.LastName}</p>
					<p><strong>Birth Date:</strong> {formatBirthDate(selectedHuman.BirthDate)}</p>
					<p><strong>Racial Descriptor:</strong> {selectedHuman.RacialDescriptor || 'Unknown'}</p>
					<p><strong>Sex:</strong> {selectedHuman.Sex || 'Unknown'}</p>

					<div class="field">
						<label class="label">Select Relationship Type</label>
						<div class="control">
							<select class="input" bind:value={relationshipType}>
								<option value="" disabled selected>Select a relationship</option>
								{#each relationshipOptions as option}
									<option value={option}>{selectedHuman.FirstName} is the {option} of {selectedHumanData.FirstName} {selectedHumanData.LastName}</option>
								{/each}
							</select>
						</div>
					</div>

					<div class="buttons">
						<button class="button is-primary" on:click={submitRelationship}>Add Relationship</button>
						<button class="button is-danger" on:click={() => selectedHuman = null}>Clear Selection</button>
					</div>
				</div>
			{/if}
		</div>
		<div class="box">
			<h3 class="title is-3">Add a member to the Family</h3>
			<!-- Search Box -->
			<div class="field">
				<div class="control">
					<input class="input" type="text" bind:value={searchQuery} placeholder="Search by name" />
				</div>
			</div>

			<!-- Humans List -->
			<table class="table is-striped is-hoverable is-fullwidth">
				<thead>
					<tr>
							<th on:click={() => toggleSort('FirstName')}>First Name</th>
							<th on:click={() => toggleSort('MiddleName')}>Middle Name</th>
							<th on:click={() => toggleSort('LastName')}>Last Name</th>
							<th on:click={() => toggleSort('BirthDate')}>Birth Date</th>
							<th on:click={() => toggleSort('RacialDescriptor')}>Racial Descriptor</th>
							<th on:click={() => toggleSort('Sex')}>Sex</th>
					</tr>
				</thead>
				<tbody>
					{#each filteredHumans as human}
						<tr on:click={() => selectHuman(human)} style="cursor: pointer;">
							<td>{human.FirstName || ''}</td>
							<td>{human.MiddleName || ''}</td>
							<td>{human.LastName || ''}</td>
							<td>{formatBirthDate(human.BirthDate)}</td>
							<td>{human.RacialDescriptor || ''}</td>
							<td>{human.Sex || ''}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	
	</div>
{/if}