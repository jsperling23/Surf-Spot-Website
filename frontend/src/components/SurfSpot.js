import React from 'react';
import {  useState, useEffect } from 'react';
import Map from './Map'


function Spot( {surfSpot} ) {
    const [collapse, setCollapse] = useState(false)
    return (
        <>
            <table className = "surfSpotTable">
                <tbody>
                    <tr>
                            <td> {surfSpot["name"]}</td>
                            <td className = "surfExpand"> <button onClick = {() => {setCollapse(!collapse)}}> + </button></td>
                        </tr>
                        { collapse ? 
                        <>
                            <tr>
                                <td>Buoy 1:</td>
                                <td> {surfSpot["buoy1"]}</td>
                            </tr>
                            <tr>
                                <td>Buoy 2:</td>
                                <td> {surfSpot["buoy2"]}</td>
                            </tr> 
                            <tr>
                                <td><strong>Ideal Period: </strong> {surfSpot["ideal"]["period"]}</td>
                                <td><strong>Ideal Swell Direction: </strong> {surfSpot["ideal"]["swellDir"]}</td>
                                <td><strong>Max Tide: </strong> {surfSpot["ideal"]["tideMax"]}</td>
                                <td><strong>Min Tide: </strong>{surfSpot["ideal"]["tideMin"]}</td>
                                <td><strong>Ideal Size: </strong>{surfSpot["ideal"]["waveSize"]}</td>
                                <td><strong>Ideal Wind: </strong>{surfSpot["ideal"]["windDir"]}</td>
                            </tr>
                            
                        </> : <></>
                        }
                </tbody>     
            </table>
        </>
    )
};

function SurfSpots() {
    const [spotData, setData] = useState(null);
    const [user, setUser] = useState(null);

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
            <Map/>
            { 
                spotData ? 
                Object.values(spotData).map((spot, key) => (
                    <Spot 
                        surfSpot = { spot }
                        key = { key }
                    />
                )):
                <p>...Loading</p> 
            }
        </div>
    )
};

export default SurfSpots;
