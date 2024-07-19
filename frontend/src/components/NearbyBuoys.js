import React from 'react';
import {  useState, useEffect } from 'react';

function Nearby( { lat, long }) {
    const [nearby, setNearby] = useState(null);

    useEffect(() => {
        const findNear = async () => {
            console.log("i'm here")
            if (lat !== 0 && long !== 0) {
                const response = await fetch(`/findBuoys?lat=${lat}&long=${long}`)
                const data = await response.text()
                const parsedData = JSON.parse(data)
                console.log(parsedData)
                //loop through parsedData and extract 
                setNearby(parsedData)                
        }}
        findNear()
    }, [lat, long])


    return(
        <>
            <div>
                    <button type="button">Nearby Buoys</button>
                </div>
                    {nearby ? (
                    <form>
                        <table className="nearbyTable">
                            <tbody>
                                <tr>
                                    <td>Distance(miles)</td>
                                    <td>Station ID</td>
                                    <td>Description</td>
                                </tr>
                                { Object.keys(nearby).length > 0 ? Object.entries(nearby).map(([key, value]) => (
                                    <tr key={key}>
                                        <td>{parseFloat(key).toFixed(2)}</td>
                                        <td>{value[0]}</td>
                                        <td>{value[1]}</td>
                                        <td>
                                            <button value={ value[0] } 
                                             type="submit">Use Station: {value[0]}
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