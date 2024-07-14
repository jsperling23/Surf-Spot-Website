import React from 'react';
import {  useState, useEffect } from 'react';

function Spot() {
    return
};

function SurfSpots() {
    const [spotData, setData] = useState(null);
    const [user, setUser] = useState(null);
    const userID = sessionStorage.getItem("userID");

    // Get all surf spots for a specific userID
    async function getSpots(user) {
        const response = await (fetch(`/surfSpot?userID=${ user }`,
                                     { method: "GET" }))
        const data = await response.json()
        return data
    };

    // Get the userID from session storage upon load
    useEffect(() => {
        const userID = sessionStorage.getItem("userID");
        if (userID) {
          setUser(userID);
          console.log(userID);
        }
      }, []);
    
    // once the user is updated, call the getSpots function to get data
    useEffect(() => {
        async function fetchData() {
            try {
                const data = await getSpots(user)
                setData(data)
                console.log(data)
            } catch (error) {
                console.error(error)
            };
            
        };
        if(user) {
            fetchData()
        };
    }, [user]);

    return (
        <div>
        </div>
    )
};

export default SurfSpots;