import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';



function NotLoggedHome() {
    console.log("component rendered")
    const [formsubmitted, setFormSubmitted] = useState(false);
    const [buoys, setBuoys] = useState(null);
    const [buoy, setBuoy] = useState("");
    const [latitude, setLatitude] = useState(null);
    const [longitude, setLongitude] = useState(null);
    const [nearby, setNearby] = useState(null);
    const navigate = useNavigate();

    // Get all buoys and set buoy data
    async function allBuoys() {
        const response = await fetch('/backend/request?stationID=all')
        const data = await response.json()
        if (response.status === 200) {
            setBuoys(data)
        } else {
            console.log(data)
        }
    }

    useEffect(() => {
        allBuoys()
    },[])

    // Handle form submission and pass the buoy state onto /buoyDisplay
    const handleSubmit = (e) => {
        console.log("submit thing");
        e.preventDefault();
        setFormSubmitted(true);
        navigate('/buoyDisplay', {state: {buoy}})
    }

    // Get the users current location
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

    // When the latitude/longitude is changed then the effect is triggered and the 
    // closest buoys to the current coordinates are displayed 
    useEffect(() => {
        const findNear = async () => {
            if (latitude !== null && longitude !== null) {
                const response = await fetch(`/backend/findBuoys?lat=${latitude}&long=${longitude}`)
                const data = await response.text()
                const parsedData = JSON.parse(data)
                setNearby(parsedData)                
        }}
        findNear()

    }, [latitude, longitude])
    

    return (
        <> 
            <article> 
                <p>Choose your buoy from a list of buoys here: <a href = "https://www.ndbc.noaa.gov/to_station.shtml">List of NOAA Buoys</a> or <a href='https://www.ndbc.noaa.gov/'>Map of NOAA Buoys</a></p>
                <p>Login or create an account to create your own surf spots and journal your sessions using those spots.</p>
                <form onSubmit={ handleSubmit } className="buoyInput">
                    <fieldset>
                        <legend>Enter Buoy Station and Press Submit</legend>
                        <label htmlFor='buoyID'>Enter your Buoy ID here:</label>
                        <input
                        id='buoyID'
                        className='buoyInput'
                        type='text'
                        maxLength='6'
                        required
                        placeholder='ex. 46327'
                        onChange={ e => setBuoy(e.target.value)}
                        autoFocus
                        ></input>

                        <button type='submit'>Submit</button>
                    </fieldset> 
                </form>
                <p>Press the button below to get the closest buoys to your location</p>
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

export default NotLoggedHome