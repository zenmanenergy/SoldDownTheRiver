<script>
	import { onMount, tick } from 'svelte';
	import {Session} from "../../Session.js";
	import { handleGetFamily } from './handleGetFamily.js';
	import { handleGetHumans } from '../Humans/handleGetHumans.js';
	import { handleGetHuman } from '../Human/handleGetHuman.js';
	import { handleAddFamilyMember } from './handleAddFamilyMember.js';
	import FamilyTreeCanvas from '../../../components/FamilyTreeCanvas.svelte';
	import { handleRemoveFamilyMember } from './handleRemoveFamilyMember.js';

	let humanId = ''; // Input for the HumanId to fetch the tree
	let error = null;

	let HumanId = null;
	let families = [];
	let Humans = [];
	let filteredHumans = [];
	let searchQuery = '';
	let selectedHumanId = null;
	let relationshipType = '';
	let relationshipOptions = [];
	let isLoading = true;
	let selectedHuman = null;
	let selectedHumanData = null;
	let sortColumn = 'LastName';
	let sortAscending = true;

	let canvas;
	const nodeWidth = 120, nodeHeight = 40, verticalSpacing = 100, horizontalSpacing = 150;
	let nodePositions = []; // new global array to store node positions
	
	// Updated drawFamilyTree: log data and show fallback message if empty
	function drawFamilyTree() {
		if (!canvas) return;
		const ctx = canvas.getContext('2d');
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		
		if (!families || families.length === 0) {
			ctx.font = '20px sans-serif';
			ctx.fillStyle = 'red';
			ctx.fillText("No family data", 20, 50);
			return;
		}
		
		// Determine vertical center
		const centerY = canvas.height / 2;
		
		// Group nodes by Depth (Depth can be negative for ancestors, 0 for self, positive for descendants)
		const groups = {};
		families.forEach(node => {
			if (!groups[node.Depth]) groups[node.Depth] = [];
			groups[node.Depth].push(node);
		});
		
		const positions = []; // each item: { node, x, y }
		for (const depth in groups) {
			const group = groups[depth];
			const d = parseInt(depth);
			// Set y based on depth offset
			const y = centerY + d * verticalSpacing;
			// Calculate horizontal start: evenly space nodes in this group
			const totalWidth = (group.length - 1) * horizontalSpacing;
			const startX = (canvas.width - totalWidth - nodeWidth) / 2;
			group.forEach((node, index) => {
				const x = startX + index * horizontalSpacing;
				positions.push({ node, x, y });
			});
			nodePositions = positions; // store for click detection
		}
		
		// Draw connecting lines with T-style for child with two parents.
		const selfPos = positions.find(pos => pos.node.Relationship === 'self');
		const spouseNode = positions.find(
			p => p.node.Relationship === 'wife' || p.node.Relationship === 'husband'
		);
		if (selfPos) {
			positions.forEach(pos => {
				// Skip drawing connection for the self and spouse nodes
				if (pos.node.Relationship === 'self' || pos.node.Relationship === 'wife' || pos.node.Relationship === 'husband') return;
				let startPoint = {}, endPoint = {};
				if (pos.node.Depth > selfPos.node.Depth) {
					// For direct children (Depth==1) and when spouse exists, use midpoint from the couple.
					if (pos.node.Depth === 1 && spouseNode) {
						startPoint = {
							x: (selfPos.x + nodeWidth/2 + spouseNode.x + nodeWidth/2) / 2,
							y: selfPos.y + nodeHeight
						};
					} else {
						startPoint = { x: selfPos.x + nodeWidth/2, y: selfPos.y + nodeHeight };
					}
					endPoint = { x: pos.x + nodeWidth/2, y: pos.y };
				} else if (pos.node.Depth < selfPos.node.Depth) {
					startPoint = { x: selfPos.x + nodeWidth/2, y: selfPos.y };
					endPoint = { x: pos.x + nodeWidth/2, y: pos.y + nodeHeight };
				} else {
					// Sibling horizontal line.
					if (pos.x > selfPos.x) {
						startPoint = { x: selfPos.x + nodeWidth, y: selfPos.y + nodeHeight/2 };
						endPoint = { x: pos.x, y: pos.y + nodeHeight/2 };
					} else {
						startPoint = { x: selfPos.x, y: selfPos.y + nodeHeight/2 };
						endPoint = { x: pos.x + nodeWidth, y: pos.y + nodeHeight/2 };
					}
				}
				ctx.beginPath();
				ctx.moveTo(startPoint.x, startPoint.y);
				ctx.lineTo(endPoint.x, endPoint.y);
				ctx.stroke();
			});
		}
		
		// Then draw each node as a rectangle with its text
		positions.forEach(pos => {
			const { node, x, y } = pos;
			ctx.strokeStyle = 'black';
			ctx.strokeRect(x, y, nodeWidth, nodeHeight);
			ctx.font = '12px sans-serif';
			ctx.fillStyle = 'black';
			const text = `${node.FirstName} ${node.LastName || ''}\n(${node.Relationship})`;
			const lines = text.split('\n');
			lines.forEach((line, index) => {
				ctx.fillText(line, x + 5, y + 15 + index * 15);
			});
		});
	}
	
	// Remove the reactive $: drawFamilyTree();

	// Utility function to get a URL parameter by name
	function getURLVariable(name) {
		return new URLSearchParams(window.location.search).get(name);
	}

	function setFamilies(data) {
		families = data;
		console.log(families);
		// wait for DOM to update so canvas is available, then draw
		tick().then(() => {
			drawFamilyTree();
		});
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
			const Human = await handleGetHuman(Session.SessionId, HumanId);
			console.log(Human)
			if (Human.isCompany==="1"){
				console.log("YES!")
				relationshipOptions = ['owner', 'employee'];
	
			} else{
				console.log("naw dog!")
				relationshipOptions = ['husband', 'wife', 'son', 'daughter', 'father', 'mother', 'brother', 'sister'];
	
			}
			await handleGetFamily(Session.SessionId, HumanId, setFamilies);
		}

		await handleGetHumans(Session.SessionId, setHumans);

		// Extract the human data from the Humans array
		selectedHumanData = Humans.find(human => human.HumanId === HumanId) || null;

		isLoading = false;
		// after onMount, ensure canvas drawing runs
		await tick();
		drawFamilyTree();
	});

	// NEW: Define a callback to remove a relationship.
	async function removeRelationship(RelatedHumanId) {
		if (confirm("Are you sure you want to remove this relationship?")) {
			const success = await handleRemoveFamilyMember(Session.SessionId, HumanId, RelatedHumanId);
			if (success) {
				alert("Relationship removed successfully!");
				window.location.reload();
			} else {
				alert("Failed to remove relationship.");
			}
		}
	}

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
			// window.location.reload();
		} else {
			alert('Failed to add relationship.');
		}
	}

	function formatBirthDate(date) {
		if (!date) return '';
		try {
			// Convert the date string into a Date object
			const dateObj = new Date(date);
			if (isNaN(dateObj)) return ''; // Ensure the date is valid

			// Extract the components
			const day = dateObj.getUTCDate();
			const month = dateObj.getUTCMonth() + 1; // Months are zero-based
			const year = dateObj.getUTCFullYear();

			// Format as m/d/yyyy
			return `${month}/${day}/${year}`;
		} catch (error) {
			console.error('Error formatting date:', error);
			return '';
		}
	}

	// New event handler for canvas click
	function handleCanvasClick(event) {
		if (!nodePositions.length) return;
		const rect = canvas.getBoundingClientRect();
		const clickX = event.clientX - rect.left;
		const clickY = event.clientY - rect.top;
		for (const pos of nodePositions) {
			if (clickX >= pos.x && clickX <= pos.x + nodeWidth &&
				clickY >= pos.y && clickY <= pos.y + nodeHeight) {
					// Navigate to /Human?HumanId={node.HumanId}
					window.location.href = `/Admin/Human?HumanId=${pos.node.HumanId}`;
					return;
			}
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
				<p><strong>Racial Descriptor:</strong> {selectedHumanData.RacialDescriptor || ''}</p>
				<p><strong>Sex:</strong> {selectedHumanData.Sex || ''}</p>
				<p><strong>Roles:</strong> {selectedHumanData.Roles.length > 0 ? selectedHumanData.Roles.join(', ') : 'No Roles'}</p>
			</div>
		{/if}

		<!-- Family Relationships Tree -->
		<!-- In case Bulma is causing canvas sizing issues, add inline style -->
		<div class="tree-container" style="padding:1rem;">
			<h3 class="title is-3">Family Tree</h3>
			<!-- Pass the onRemove callback -->
			<FamilyTreeCanvas {families} onRemove={removeRelationship} />
			<!-- Optionally keep selected human display if needed -->
			{#if selectedHuman}
			<hr>
				<div class="selected-human">
					<h4 class="title is-4">Selected Human</h4>
					<p><strong>Name:</strong> {selectedHuman.FirstName} {selectedHuman.MiddleName} {selectedHuman.LastName}</p>
					<p><strong>Birth Date:</strong> {formatBirthDate(selectedHuman.BirthDate)}</p>
					<p><strong>Racial Descriptor:</strong> {selectedHuman.RacialDescriptor || ''}</p>
					<p><strong>Sex:</strong> {selectedHuman.Sex || ''}</p>

					<div class="field">
						<label class="label" for="relationshipType">Select Relationship Type</label>
						<div class="control">
							<select id="relationshipType" class="input" bind:value={relationshipType}>
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
					{#each filteredHumans.slice(0, 10) as human}
						<tr on:click={() => selectHuman(human)} style="cursor: pointer;">
							<td>{human.FirstName || ''}</td>
							<td>{human.MiddleName || ''}</td>
							<td>{human.LastName || ''}</td>
							<td>{formatBirthDate(human.BirthDate) || ''}</td>
							<td>{human.RacialDescriptor || ''}</td>
							<td>{human.Sex || ''}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	
	</div>
{/if}