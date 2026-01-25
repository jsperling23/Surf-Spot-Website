import React from 'react';
import {  useEffect } from 'react';

function Nearby( { lat, long, nearby, setNearby, fillBuoys }) {
    useEffect(() => {
        const findNear = async () => {
            if (lat !== 0 && long !== 0) {
                const response = await fetch(`/backend/find_buoys?lat=${lat}&long=${long}`)
                const data = await response.text()
                const parsedData = JSON.parse(data)
                console.log(parsedData)
                //loop through parsedData and extract 
                setNearby(parsedData)                
        }}
        findNear()
    }, [lat, long, setNearby])


    return(
        <>
    
            {nearby ? (
            <form>
                <table className="nearbyTable">
                    <tbody>
                        <tr>
                            <td><strong>Distance(miles)</strong></td>
                            <td><strong>Station ID</strong></td>
                            <td><strong>Description</strong></td>
                        </tr>
                        { Object.keys(nearby).length > 0 ? Object.entries(nearby).map(([key, value]) => (
                            <tr key={key}>
                                <td>{parseFloat(key).toFixed(2)}</td>
                                <td>{value[0]}</td>
                                <td>{value[1]}</td>
                                <td>
                                    <button type='button' value={ value[0] } 
                                        onClick={ () => fillBuoys(value[0]) }>Use Station: {value[0]}
                                    </button>
                                </td>
                            </tr>
                        )): <tr><td>No Buoys Nearby</td></tr>}
                        
                    </tbody>
                </table>
            </form>
                ) : null}  
        </>
    )
};

export default Nearby;