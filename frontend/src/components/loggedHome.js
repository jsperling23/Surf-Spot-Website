import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import SurfSpots from './SurfSpot';
import Sessions from './Sessions'


function LoggedHome() {
    console.log("component rendered")
    const [formsubmitted, setFormSubmitted] = useState(false);
    const [buoy, setBuoy] = useState("");
    const [latitude, setLatitude] = useState(null)
    const [longitude, setLongitude] = useState(null)
    const [nearby, setNearby] = useState(null)
    const navigate = useNavigate();


    //Handle form submission and pass the buoy state onto /buoyDisplay
    const handleSubmit = (e) => {
        console.log("submit thing");
        e.preventDefault();
        setFormSubmitted(true);
        navigate('/buoyDisplay', {state: {buoy}})
    }

    //Get the users current location
    const getLocation = () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(success)
        } else {
            alert("Geolocation not accessible using this browser")
        }
    };
    const success = (pos) => {
            const coords = pos.coords
            setLatitude(coords.latitude)
            setLongitude(coords.longitude)
    };

    //When the latitude/longitude is changed then the effect is triggered and the 
    //closest buoys to the current coordinates are displayed 
    useEffect(() => {
        const findNear = async () => {
            if (latitude !== null && longitude !== null) {
                const response = await fetch(`/backend/find_buoys?lat=${latitude}&long=${longitude}`)
                const data = await response.text()
                const parsedData = JSON.parse(data)

                //loop through parsedData and extract 
                setNearby(parsedData)                
        }}
        findNear()

    }, [latitude, longitude])
    

    return (
        <>
            <article className='loggedHome'> 
                <div className='surfStuff'>
                    <SurfSpots/>
                    <Sessions/>
                </div>
                <p>Find Nearby Buoys</p>
                <div>
                    <button type="button" onClick={ getLocation }>Find Nearby Buoys</button>
                </div>
                    {nearby ? (
                    <form onSubmit={ handleSubmit }>
                        <table className="nearbyTable">
                            <tbody>
                                <tr>
                                    <td>Distance(miles)</td>
                                    <td>Station ID</td>
                                    <td>Description</td>
                                </tr>
                                {Object.entries(nearby).map(([key, value]) => (
                                    <tr key={key}>
                                        <td>{parseFloat(key).toFixed(2)}</td>
                                        <td>{value[0]}</td>
                                        <td>{value[1]}</td>
                                        <td>
                                            <button id='nearbyButton' value={ value[0] } 
                                                onClick={ e => setBuoy(e.target.value)} type="submit">Use Station: {value[0]}
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </form>
                        ) : null}         
            </article>
        </>
    )
};

export default LoggedHome