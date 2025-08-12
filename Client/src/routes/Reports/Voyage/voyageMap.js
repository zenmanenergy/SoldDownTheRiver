import { baseURL } from '../../Settings';
import { SuperFetch } from '../../SuperFetch';

let map = null;
let usaOutlineLayer = null;
let shipMarker = null;
let shipAnimationFrame = null;

export function initMap(mapContainer, Voyage, Locations, usaOutlineGeoJson) {
	if (!window.L || !mapContainer) return;
	if (map) {
		map.remove();
		map = null;
	}
	const [lat, lng] = getFirstLatLng(Voyage, Locations);
	map = window.L.map(mapContainer).setView([lat, lng], 5);
	window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		maxZoom: 18,
		attribution: '© OpenStreetMap contributors'
	}).addTo(map);
	addMapMarkers(Voyage, Locations);
	if (usaOutlineGeoJson) {
		showUsaOutline(usaOutlineGeoJson);
	}
}

// Remove sanitizeUsaGeoJson and use the raw geojson
export function showUsaOutline(geojson) {
	if (!map || !window.L || !geojson) return;
	if (usaOutlineLayer) {
		map.removeLayer(usaOutlineLayer);
		usaOutlineLayer = null;
	}
	usaOutlineLayer = window.L.geoJSON(geojson, {
		style: {
			color: "#1976d2",
			weight: 0,
			fill: false,
			fillColor: "#1976d2",
			fillOpacity: 0
		}
	}).addTo(map);

	// Fit map to polygon bounds
	try {
		map.fitBounds(usaOutlineLayer.getBounds());
	} catch (e) {
		// If there is an error, do nothing
	}
}

export function addMapMarkers(Voyage, Locations) {
	if (!map || !window.L) return;
	const L = window.L;
	// Remove existing markers and polylines
	if (map._markerLayer) {
		map.removeLayer(map._markerLayer);
		map._markerLayer = null;
	}
	if (map._routeLine) {
		map.removeLayer(map._routeLine);
		map._routeLine = null;
	}
	const markers = [];
	const types = [
		{ type: 'Start', id: Voyage.StartLocationId, color: 'blue' },
		{ type: 'Customs', id: Voyage.CustomsLocationId, color: 'orange' },
		{ type: 'End', id: Voyage.EndLocationId, color: 'red' }
	];
	const points = [];
	for (const t of types) {
		const pos = getLocationLatLngObj(t.id, Locations);
		if (pos) {
			const marker = L.marker([pos.lat, pos.lng], {
				icon: L.icon({
					iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-${t.color}.png`,
					iconSize: [25, 41],
					iconAnchor: [12, 41],
					popupAnchor: [1, -34],
					shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png'
				})
			}).bindPopup(`${t.type} Location`);
			markers.push(marker);
			points.push([pos.lat, pos.lng]);
		}
	}
	if (markers.length) {
		const group = window.L.featureGroup(markers).addTo(map);
		map._markerLayer = group;
		map.fitBounds(group.getBounds().pad(0.3));
	}
	// Remove this block to prevent drawing the default black dotted line
	// if (points.length >= 2) {
	// 	const polyline = L.polyline(points, { color: 'navy', weight: 3, dashArray: '6, 8' }).addTo(map);
	// 	map._routeLine = polyline;
	// }
}

function getFirstLatLng(Voyage, Locations) {
	const ids = [Voyage.StartLocationId, Voyage.CustomsLocationId, Voyage.EndLocationId];
	for (const id of ids) {
		const loc = Locations.find(l => l.LocationId === id);
		if (loc && loc.Latitude && loc.Longitude) {
			return [parseFloat(loc.Latitude), parseFloat(loc.Longitude)];
		}
	}
	return [0, 0];
}

function getLocationLatLngObj(locationId, Locations) {
	const location = Locations.find(l => l.LocationId === locationId);
	if (location && location.Latitude && location.Longitude) {
		return {
			lat: parseFloat(location.Latitude),
			lng: parseFloat(location.Longitude)
		};
	}
	return null;
}

export async function loadLeaflet() {
	if (typeof window === 'undefined') return;
	if (window.L) return;

	// Load Leaflet CSS
	if (!document.querySelector('link[href*="leaflet.css"]')) {
		const leafletCss = document.createElement('link');
		leafletCss.rel = 'stylesheet';
		leafletCss.href = 'https://unpkg.com/leaflet@1.7.1/dist/leaflet.css';
		document.head.appendChild(leafletCss);
	}

	// Load Leaflet JS
	if (!document.querySelector('script[src*="leaflet.js"]')) {
		await new Promise((resolve) => {
			const leafletScript = document.createElement('script');
			leafletScript.src = 'https://unpkg.com/leaflet@1.7.1/dist/leaflet.js';
			leafletScript.onload = resolve;
			document.body.appendChild(leafletScript);
		});
	}
}

export function getMap() {
	return map;
}

/**
 * Animate a ship icon along the given path.
 * @param {Array<[number, number]>} pathPoints Array of [lat, lng]
 */
export function animateShipAlongPath(pathPoints) {
	if (!map || !window.L || !Array.isArray(pathPoints) || pathPoints.length < 2) return;

	// Remove previous ship marker and animation
	if (shipMarker) {
		map.removeLayer(shipMarker);
		shipMarker = null;
	}
	if (shipAnimationFrame) {
		cancelAnimationFrame(shipAnimationFrame);
		shipAnimationFrame = null;
	}

	// Use an 1800s schooner icon (public domain or open-licensed)
	const shipIcon = window.L.icon({
		iconUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Sail_plan_barque.svg/1920px-Sail_plan_barque.svg.png',
		iconSize: [48, 48],
		iconAnchor: [24, 24],
	});

	let progress = 0;
	const steps = 500; // Number of animation steps
	let segment = 0;
	let segProgress = 0;

	function interpolate(p1, p2, t) {
		return [
			p1[0] + (p2[0] - p1[0]) * t,
			p1[1] + (p2[1] - p1[1]) * t
		];
	}

	function animate() {
		const totalSegments = pathPoints.length - 1;
		const segLen = 1 / totalSegments;
		const t = progress / steps;
		segment = Math.floor(t * totalSegments);
		segProgress = (t - segment * segLen) / segLen;

		if (segment >= totalSegments) {
			// End of path
			if (shipMarker) {
				shipMarker.setLatLng(pathPoints[pathPoints.length - 1]);
			}
			return;
		}

		const pos = interpolate(pathPoints[segment], pathPoints[segment + 1], segProgress);

		if (!shipMarker) {
			shipMarker = window.L.marker(pos, { icon: shipIcon, zIndexOffset: 1000 }).addTo(map);
		} else {
			shipMarker.setLatLng(pos);
		}

		progress++;
		if (progress <= steps) {
			shipAnimationFrame = requestAnimationFrame(animate);
		}
	}

	animate();
}

/**
 * Draw a path from start to end that leaves the polygon at the closest edge, 
 * travels outside the polygon, then re-enters at the closest edge to the end.
 * Both start and end may be inside the polygon.
 * @param {[number, number]} start [lat, lng]
 * @param {[number, number]} end [lat, lng]
 * @param {object} polygonGeoJson GeoJSON Polygon
 */
export function drawPathOutsidePolygon(start, end, polygonGeoJson) {
	if (!map || !window.L || !polygonGeoJson) return;

	const polygon = polygonGeoJson.features[0].geometry;
	const coords = polygon.coordinates[0];

	// Helper: convert [lng, lat] to [lat, lng]
	const toLatLng = ([lng, lat]) => [lat, lng];

	// Helper: convert [lat, lng] to [lng, lat]
	const toLngLat = ([lat, lng]) => [lng, lat];

	// Find nearest polygon edge point to start and end
	let minStartDist = Infinity, minEndDist = Infinity;
	let nearestStart, nearestEnd;
	for (const pt of coords) {
		const dStart = distanceLatLng(start, toLatLng(pt));
		const dEnd = distanceLatLng(end, toLatLng(pt));
		if (dStart < minStartDist) {
			minStartDist = dStart;
			nearestStart = toLatLng(pt);
		}
		if (dEnd < minEndDist) {
			minEndDist = dEnd;
			nearestEnd = toLatLng(pt);
		}
	}
	// Get the polygon path between nearestStart and nearestEnd (shortest direction)
	const idxStart = coords.findIndex(pt => distanceLatLng(start, toLatLng(pt)) === minStartDist);
	const idxEnd = coords.findIndex(pt => distanceLatLng(end, toLatLng(pt)) === minEndDist);

	let path1 = [], path2 = [];
	if (idxStart < idxEnd) {
		path1 = coords.slice(idxStart, idxEnd + 1);
		path2 = coords.slice(idxEnd).concat(coords.slice(0, idxStart + 1));
	} else {
		path1 = coords.slice(idxEnd, idxStart + 1).reverse();
		path2 = coords.slice(idxStart).concat(coords.slice(0, idxEnd + 1)).reverse();
	}
	// Choose the shorter path
	const len1 = path1.length;
	const len2 = path2.length;
	const bestPath = len1 <= len2 ? path1 : path2;

	const pathPoints = [
		start,
		nearestStart,
		...bestPath.map(toLatLng),
		nearestEnd,
		end
	];

	// Remove any previous path polylines if needed (optional)
	if (map._voyagePathLine) {
		map.removeLayer(map._voyagePathLine);
		map._voyagePathLine = null;
	}

	map._voyagePathLine = window.L.polyline(pathPoints, {
		color: 'orange',
		weight: 4,
		dashArray: '10, 10'
	}).addTo(map);

	// Animate the ship along the path
	animateShipAlongPath(pathPoints);
}

// Helper: Haversine distance between [lat, lng]
function distanceLatLng(a, b) {
	const toRad = x => x * Math.PI / 180;
	const R = 6371; // km
	const dLat = toRad(b[0] - a[0]);
	const dLng = toRad(b[1] - a[1]);
	const lat1 = toRad(a[0]);
	const lat2 = toRad(b[0]);
	const aVal = Math.sin(dLat / 2) ** 2 +
		Math.sin(dLng / 2) ** 2 * Math.cos(lat1) * Math.cos(lat2);
	const c = 2 * Math.atan2(Math.sqrt(aVal), Math.sqrt(1 - aVal));
	return R * c;
}