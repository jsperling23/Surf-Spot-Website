import React from 'react';
import {  useEffect, useRef } from 'react';
import L from 'leaflet';

function HomeMap() {
    const mapRef = useRef(null)
    const markerRef = useRef([])
    
    useEffect(() => {
        if(mapRef.current) return;

        const map = L.map('map').setView([37.77, 122.41], 1);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        mapRef.current = map
        const popup = L.popup();
        
        /*
        function onMapClick(e) {
            popup
                .setLatLng(e.latlng)
                .setContent("Chosen coordinates:  " + e.latlng.wrap().toString())
                .openOn(mapRef.current);
        }

        mapRef.current.on('click', onMapClick);
        */
      }, []);

    return (
        <>
            <div id="map"></div>
        </>
        );
    };

export default HomeMap;