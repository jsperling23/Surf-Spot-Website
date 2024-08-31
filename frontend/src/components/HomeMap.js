import React from 'react';
import {  useEffect, useRef } from 'react';
import L from 'leaflet';

function HomeMap( { spotData, buoyData, setMapButton } ) {
    const mapRef = useRef(null)
    const markerRef = useRef([])
    
    useEffect(() => {
        if(mapRef.current) return;

        const map = L.map('map').setView([37.77, -122.41], 3);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        mapRef.current = map
      }, []);

        
    useEffect(() => {
        markerRef.current.forEach(marker => mapRef.current.removeLayer(marker));
        markerRef.current = [];

        if (spotData) {
            Object.entries(spotData).forEach(([key, value]) => {
                console.log(value.name)
                const latitude = value.latitude
                const longitude = value.longitude
                const marker = L.marker([latitude, longitude]).addTo(mapRef.current)
                marker.bindPopup(`<strong>${value.name}</strong>`)
                markerRef.current.push(marker)
            })
        };

        if (buoyData) {
            Object.entries(buoyData).forEach(([key, value]) => {
                const latitude = value.latitude
                const longitude = value.longitude
                const marker = L.marker([latitude, longitude]).addTo(mapRef.current)
                marker.bindPopup(`<strong>${value.description}: 
                                </strong>
                                <br/>
                                <p>${value.stationID}</p>
                                <button id="mapButton" value=${value.stationID}>Use Station</button>`
                                )
                markerRef.current.push(marker)

                //add event listener for button click
                marker.on("popupopen", () => {
                    document.getElementById("mapButton").addEventListener("click", (e) => {
                        setMapButton(e.target.value)
                    })
                });
            })
        };

        }, [spotData, buoyData])

    return (
        <>
            <div id="map"></div>
        </>
        );
    };

export default HomeMap;