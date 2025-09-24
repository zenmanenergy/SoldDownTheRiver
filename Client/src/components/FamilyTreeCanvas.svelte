<script>
	import { onMount, tick } from 'svelte';
	export let families = [];
	export let width = 800;
	export let height = 600;
	// Callback when a remove is requested for a node.
	export let onRemove = null; 
	export let BaseHref = "/Admin/Human"; // Default value

	let canvas;
	let nodePositions = []; // used for click detection

	const nodeWidth = 120, nodeHeight = 40, verticalSpacing = 100, horizontalSpacing = 150;
	const removeBoxSize = 15; // area of "X" button

	function drawFamilyTree() {
	if (!canvas) return;
	const ctx = canvas.getContext('2d');
	ctx.clearRect(0, 0, width, height);

	if (!families || families.length === 0) {
		ctx.font = '20px sans-serif';
		ctx.fillStyle = 'red';
		ctx.fillText("No family data", 20, 50);
		return;
	}

	const centerY = height / 2;

	// Group nodes by Depth
	const groups = {};
	families.forEach(node => {
		if (!groups[node.Depth]) groups[node.Depth] = [];
		groups[node.Depth].push(node);
	});

	const positions = [];
	for (const depth in groups) {
		const group = groups[depth];
		const d = parseInt(depth);
		const y = centerY + d * verticalSpacing;
		const totalWidth = (group.length - 1) * horizontalSpacing;
		const startX = (width - totalWidth - nodeWidth) / 2;
		group.forEach((node, index) => {
		const x = startX + index * horizontalSpacing;
		positions.push({ node, x, y });
		});
	}
	nodePositions = positions;

	// Parent-child connections:
	positions.forEach(pos => {
		if (pos.node.Relationship === 'self') return;
		let parentCandidate = null;
		if (pos.node.Depth > 0) {
		const candidates = positions.filter(p => p.node.Depth === pos.node.Depth - 1);
		if (candidates.length) {
			parentCandidate = candidates.reduce((prev, curr) =>
			Math.abs(curr.x - pos.x) < Math.abs(prev.x - pos.x) ? curr : prev
			);
			const start = { x: parentCandidate.x + nodeWidth/2, y: parentCandidate.y + nodeHeight };
			const end	 = { x: pos.x + nodeWidth/2, y: pos.y };
			ctx.beginPath();
			ctx.moveTo(start.x, start.y);
			ctx.lineTo(end.x, end.y);
			ctx.stroke();
		}
		} else if (pos.node.Depth < 0) {
		const candidates = positions.filter(p => p.node.Depth === pos.node.Depth + 1);
		if (candidates.length) {
			parentCandidate = candidates.reduce((prev, curr) =>
			Math.abs(curr.x - pos.x) < Math.abs(prev.x - pos.x) ? curr : prev
			);
			const start = { x: parentCandidate.x + nodeWidth/2, y: parentCandidate.y };
			const end	 = { x: pos.x + nodeWidth/2, y: pos.y + nodeHeight };
			ctx.beginPath();
			ctx.moveTo(start.x, start.y);
			ctx.lineTo(end.x, end.y);
			ctx.stroke();
		}
		}
	});

	// Sibling connections
	for (const depth in groups) {
		const groupNodes = groups[depth];
		if (groupNodes.length > 1) {
		const sortedPositions = positions.filter(p => p.node.Depth == depth).sort((a, b) => a.x - b.x);
		for (let i = 0; i < sortedPositions.length - 1; i++) {
			const leftPos = sortedPositions[i];
			const rightPos = sortedPositions[i+1];
			const start = { x: leftPos.x + nodeWidth, y: leftPos.y + nodeHeight/2 };
			const end = { x: rightPos.x, y: rightPos.y + nodeHeight/2 };
			ctx.beginPath();
			ctx.moveTo(start.x, start.y);
			ctx.lineTo(end.x, end.y);
			ctx.stroke();
		}
		}
	}

	// Draw nodes and add "X" for removal in the top right corner.
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
		// Draw removal "X" at the top-right corner.
		ctx.fillStyle = 'red';
		ctx.font = 'bold 14px sans-serif';
		ctx.fillText('X', x + nodeWidth - removeBoxSize, y + removeBoxSize);
	});
	}

	$: tick().then(() => {
	drawFamilyTree();
	});

	function handleCanvasClick(event) {
	if (!nodePositions.length) return;
	const rect = canvas.getBoundingClientRect();
	const clickX = event.clientX - rect.left;
	const clickY = event.clientY - rect.top;
	for (const pos of nodePositions) {
			const { x, y } = pos;
			// if click is within the node rectangle...
			if (clickX >= x && clickX <= x + nodeWidth &&
				clickY >= y && clickY <= y + nodeHeight) {
				// ...check if it's inside the removal "X" area (top-right corner)
				if (clickX >= x + nodeWidth - removeBoxSize && clickX <= x + nodeWidth &&
					clickY >= y && clickY <= y + removeBoxSize) {
					console.log("onRemove")
					if (onRemove) {
						onRemove(pos.node.HumanId);
					}
				} else {
					window.location.href = `${BaseHref}?HumanId=${pos.node.HumanId}`;
				}
				return;
			}
		}
	}

	onMount(() => {
	drawFamilyTree();
	});
</script>

<canvas bind:this={canvas} on:click={handleCanvasClick} width={width} height={height} style="border:1px solid #ccc;"></canvas>
