import { useState, useEffect } from 'react';
import { useNavigate, NavLink } from 'react-router-dom';



function NotLoggedHome() {
    console.log("component rendered")
    const [formsubmitted, setFormSubmitted] = useState(false);
    const [buoy, setBuoy] = useState("");
    const [latitude, setLatitude] = useState(null);
    const [longitude, setLongitude] = useState(null);
    const [nearby, setNearby] = useState(null);
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
                const response = await fetch(`/findBuoys?lat=${latitude}&long=${longitude}`)
                const data = await response.text()
                const parsedData = JSON.parse(data)

                //loop through parsedData and extract 
                setNearby(parsedData)                
        }}
        findNear()

    }, [latitude, longitude])
    

    return (
        <> 
            <article> 
                <p>If you're a new user, give yourself at least 5 minutes to find and enter your buoy station ID.</p>
                <p>Choose your buoy from a list of buoys here: <a href = "https://www.ndbc.noaa.gov/to_station.shtml">List of NOAA Buoys (requires knowledge of buoy locations)</a> or <a href='https://www.ndbc.noaa.gov/'>Map of NOAA Buoys (requires knowledge of using maps)</a></p>
                <p>Get buoy data by filling out the form below after finding the station ID of your buoy of choice </p>
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
                <p>You can also find the buoys closest using your current location or coordinates of your choice</p>
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
                                            <button value={ value[0] } 
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