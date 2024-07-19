import React from 'react';
import {  useEffect, useRef } from 'react';
import L from 'leaflet';

function Map( { setLat, setLong } ) {
    const mapRef = useRef(null)
    
    useEffect(() => {
        if(mapRef.current) return;

        const map = L.map('map').setView([37.77, 122.41], 0);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        mapRef.current = map
        const popup = L.popup();

        function onMapClick(e) {
            popup
                .setLatLng(e.latlng)
                .setContent("Chosen coordinates:  " + e.latlng.toString())
                .openOn(mapRef.current);
                setLat(e.latlng.lat.toFixed(2))
                setLong(e.latlng.lng.toFixed(2))
        }

        mapRef.current.on('click', onMapClick);
      }, []);

    return (
        <>
            <div id="map"></div>
        </>
        );
    };

export default Map;