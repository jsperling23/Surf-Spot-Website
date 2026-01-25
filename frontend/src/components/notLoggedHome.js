import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import HomeMap from './HomeMap';



function NotLoggedHome() {
    console.log("component rendered")
    const [formsubmitted, setFormSubmitted] = useState(false);
    const [buoys, setBuoys] = useState(null);
    const [mapButton, setMapButton] = useState(null)
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

    useEffect(() => {
        if (mapButton) {
                console.log(`StationID: ${mapButton}`)
                navigate('/buoyDisplay', {state: {mapButton}})
        };
    }, [mapButton])


    // Handle form submission and pass the buoy state onto /buoyDisplay
    const handleSubmit = (e) => {
        console.log(buoy);
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
                const response = await fetch(`/backend/find_buoys?lat=${latitude}&long=${longitude}`)
                const data = await response.text()
                const parsedData = JSON.parse(data)
                setNearby(parsedData)                
        }}
        findNear()

    }, [latitude, longitude])
    

    return (
        <> 
            <article> 
                <p>Choose a buoy from the map below to get current conditions</p>
                <p>Login or create an account to create your own surf spots and journal your sessions</p>
                {buoys ? <HomeMap buoyData = { buoys } setMapButton = { setMapButton }/> : <p>...loading</p>}
                <form onSubmit={ handleSubmit } className="buoyInput">
                    <fieldset>
                        <legend>You can also manually enter the station ID</legend>
                        <label htmlFor='buoyID'>Station ID:</label>
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