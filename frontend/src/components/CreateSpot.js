import React from 'react';
import {  useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Map from './CreateMap';
import Nearby from './NearbyBuoys'
import CreateMap from './CreateMap';

function CreateSpot() {
    const [lat, setLat] = useState(0);
    const [long, setLong] = useState(0);
    const [spotName, setName] = useState(null);
    const [buoy1, setBuoy1] = useState(null);
    const [buoy2, setBuoy2] = useState(null);
    const [user, setUser] = useState(null)
    const [nearby, setNearby] = useState(null)
    const navigate = useNavigate();

    // Get the userID from session storage upon load
    useEffect(() => {
        const userID = sessionStorage.getItem("userID");
        if (userID) {
          setUser(userID);
          console.log(userID);
        }

      }, []);

    async function handleSubmit(e){
        e.preventDefault();

        const createSpot = await fetch("/surfSpot",
            {method: 'POST',
            headers: {
                'Content-Type': 'application/json'},
            body: JSON.stringify({
                    userID: user,
                    name: spotName,
                    latitude: lat,
                    longitude: long,
                    firstBuoyID: buoy1,
                    secondBuoyID: buoy2
                }),
            credentials: 'include'
            });
            if (createSpot.status === 201) {
                console.log(createSpot.status)
                alert("Surf Spot Created!")
                navigate('/');
            } else {
                const responseData = await createSpot.json();
                console.log(responseData)
                alert(responseData.result)
            };
    };
    return(
        <>
            <CreateMap setLat = { setLat } setLong = { setLong } nearby = { nearby} />
            <form onSubmit={ handleSubmit }>
                <fieldset>
                    <legend>Enter latitude and longitude and fill out the following fields</legend>
                    <label htmlFor='spotName'>Name: </label>
                    <input
                    type='text'
                    required
                    maxLength='100'
                    placeholder="ex. Pipeline"
                    onChange={e => setName(e.target.value)}>
                    </input>
                    <br></br>
                    <label htmlFor='latitude'>Latitude: </label>
                    <input
                    type='number'
                    required
                    maxLength='10'
                    placeholder={ lat }
                    value={ lat }
                    onChange={e => setLat(e.target.value)}>
                    </input>
                    <br></br>
                    <label htmlFor='latitude'>Longitude: </label>
                    <input
                    type='number'
                    required
                    maxLength='10'
                    placeholder={ long }
                    value={ long }
                    onChange={e => setLong(e.target.value)}>
                    </input>
                    <br></br>
                    <label htmlFor='buoy1'>First Buoy: </label>
                    <input
                    type='text'
                    maxLength='10'
                    placeholder='ex.46237'
                    onChange={e => setBuoy1(e.target.value)}>
                    </input>
                    <br></br>
                    <label htmlFor='buoy2'>Second Buoy: </label>
                    <input
                    type='text'
                    maxLength='10'
                    placeholder='ex.46237'
                    onChange={e => setBuoy2(e.target.value)}>
                    </input>
                    <br></br>
                    <br></br>
                    <button type='submit'>Submit</button>
                </fieldset>
            </form>
            <div>{lat != 0 && long !=0 ? <Nearby lat = { lat } long = { long } 
                  setNearby = { setNearby } nearby = { nearby }/> : <></>}
            </div>
            
        </>
    )
};

export default CreateSpot;