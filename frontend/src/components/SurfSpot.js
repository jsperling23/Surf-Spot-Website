import React from 'react';
import {  useState, useEffect } from 'react';
import HomeMap from './HomeMap'
import Sessions from './Sessions'


function Spot( { surfSpot, updateSpots } ) {
    const [collapse, setCollapse] = useState(false)
    const spotID = surfSpot["spotID"]

    async function handleDelete(e) {
        e.preventDefault();
        const decision = window.confirm("Are you sure you want to delete this spot?");
        if (!decision) return;
        const deleteSpot = await fetch(`/surfSpot?spotID=${spotID}`,
            {method: 'DELETE', credentials: 'include'});
            if (deleteSpot.status === 201) {
                const response = await deleteSpot.json()
                console.log(response);
                updateSpots(spotID);
            } else {
                const responseData = await deleteSpot.json();
                console.log(responseData)
                alert(responseData.result)
            };
    };
    return (
        <>
            <table className = "surfSpotTable">
                <tbody>
                    <tr>
                            <td> {surfSpot["name"]}</td>
                            <td className = "surfExpand" colSpan='5'> 
                                <button onClick = {() => {setCollapse(!collapse)}}> + </button>
                            </td>
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
                            <tr>
                                <td colSpan='5'> 
                                    <button onClick = { handleDelete }> Delete Spot </button>
                                </td>
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

    function updateSpots(id) {
        setData(() => {
            const updated = {...spotData};
            console.log("Now deleted: ", updated[id])
            delete updated[id]
            return updated
        })
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
            } catch (error) {
                console.error(error)
            };
            
        };
        if(user) {
            fetchData()
        };
    }, [user]);

    
    return (
        
            <div className='surfStuff'>
                <HomeMap/>
                <Sessions/>             
                    <div>
                        { 
                            spotData ? 
                            Object.values(spotData).map((spot, key) => (
                                <Spot 
                                    surfSpot = { spot }
                                    key = { key }
                                    updateSpots = { updateSpots }
                                />
                            )):
                            <p>...Loading</p> 
                        }
                    </div>
            </div>
        
    )
};

export default SurfSpots;
