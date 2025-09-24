<script>
    import { onMount } from 'svelte';
    import * as timelineMap from './timelineMap.js';
    import usaOutlineGeoJson from './usa_continental_outline.js';

    export let Voyage = {};
    export let Locations = [];
    export let captureMode = false; // Optional: enable capture mode from parent

    let mapContainer;
    let mapInitialized = false;
    let mapClickHandler = null;

    // Helper to get start and end lat/lng
    function getStartEndLatLng() {
        const startLoc = Locations.find(l => l.LocationId === Voyage.StartLocationId);
        const endLoc = Locations.find(l => l.LocationId === Voyage.EndLocationId);
        if (startLoc && endLoc && startLoc.Latitude && startLoc.Longitude && endLoc.Latitude && endLoc.Longitude) {
            return {
                start: [parseFloat(startLoc.Latitude), parseFloat(startLoc.Longitude)],
                end: [parseFloat(endLoc.Latitude), parseFloat(endLoc.Longitude)]
            };
        }
        return null;
    }

    function onMapClick(e) {
        const { lat, lng } = e.latlng;
        // Log in [lng, lat] format for polygon capture
        console.log(`[${lng}, ${lat}],`);
    }

    function setupCaptureMode() {
        if (captureMode && window.L && timelineMap.getMap()) {
            const map = timelineMap.getMap();
            map.on('click', onMapClick);
        }
    }

    function removeCaptureMode() {
        if (window.L && timelineMap.getMap()) {
            const map = timelineMap.getMap();
            map.off('click', onMapClick);
        }
    }

    // Watch for captureMode changes
    $: if (mapInitialized) {
        if (captureMode) {
            setupCaptureMode();
        } else {
            removeCaptureMode();
        }
    }

    // Redraw path and markers when Voyage or Locations change
    $: if (mapInitialized && Locations.length > 0) {
        console.log('TimelineMap: Locations passed to map:', Locations);
        timelineMap.addMapMarkers(Voyage, Locations);
        const latlng = getStartEndLatLng();
        if (latlng) {
            timelineMap.drawPathOutsidePolygon(latlng.start, latlng.end, usaOutlineGeoJson);
        }
    }

    onMount(async () => {
        await timelineMap.loadLeaflet();
        mapInitialized = true;
        setTimeout(() => {
            timelineMap.initMap(mapContainer, Voyage, Locations, usaOutlineGeoJson);
            timelineMap.showUsaOutline(usaOutlineGeoJson);
            // Draw path on mount if possible
            const latlng = getStartEndLatLng();
            if (latlng) {
                timelineMap.drawPathOutsidePolygon(latlng.start, latlng.end, usaOutlineGeoJson);
            }
            if (captureMode) {
                setupCaptureMode();
            }
        }, 0);
    });
</script>

<div bind:this={mapContainer} id="osm-map" style="height:350px;width:100%;border-radius:8px;border:1px solid #e9ecef;"></div>
