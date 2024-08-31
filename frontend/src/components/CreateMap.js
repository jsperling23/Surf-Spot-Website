import React from 'react';
import { renderToString } from 'react-dom/server'
import {  useEffect, useRef } from 'react';
import L from 'leaflet';

function CreateMap( { setLat, setLong, nearby, fillBuoys } ) {
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
        
        function onMapClick(e) {
            popup
                .setLatLng(e.latlng)
                .setContent("Chosen coordinates:  " + e.latlng.wrap().toString())
                .openOn(mapRef.current);
                setLat(e.latlng.wrap().lat.toFixed(2))
                setLong(e.latlng.wrap().lng.toFixed(2))
        }

        mapRef.current.on('click', onMapClick);

      }, [setLat, setLong]);
    
      useEffect(() => {
        markerRef.current.forEach(marker => mapRef.current.removeLayer(marker));
        markerRef.current = [];

        if (nearby) {
            Object.entries(nearby).map(([key, value]) => {
                const latitude = value[2]
                const longitude = value[3]
                const marker = L.marker([latitude, longitude]).addTo(mapRef.current);
                marker.bindPopup(`<strong>Station ID: ${value[0]}
                    </strong>
                    <br/>
                    <button id=${key} value=${value[0]}>Use Station</button>`
                    );
                markerRef.current.push(marker);

                marker.on("popupopen", () => {
                    document.getElementById(key).addEventListener("click", (e) => {
                        console.log("Clicked: ", e.target.value)
                        fillBuoys(e.target.value)
                    })
                });
            })
        };
      }, [nearby])

    return (
        <>
            <div id="map"></div>
        </>
        );
    };

export default CreateMap;