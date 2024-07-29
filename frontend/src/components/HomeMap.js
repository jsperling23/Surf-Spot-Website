import React from 'react';
import {  useEffect, useRef } from 'react';
import L from 'leaflet';

function HomeMap( { spotData } ) {
    const mapRef = useRef(null)
    const markerRef = useRef([])
    
    useEffect(() => {
        if(mapRef.current) return;

        const map = L.map('map').setView([37.77, -122.41], 8);
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
    
    useEffect(() => {
        markerRef.current.forEach(marker => mapRef.current.removeLayer(marker));
        markerRef.current = [];

        if (spotData) {
            Object.entries(spotData).forEach(([key, value]) => {
                const latitude = value.latitude
                const longitude = value.longitude
                const marker = L.marker([latitude, longitude]).addTo(mapRef.current)
                marker.bindPopup(value.name)
                markerRef.current.push(marker)
            })
        };
        }, [spotData])

    return (
        <>
            <div id="map"></div>
        </>
        );
    };

export default HomeMap;