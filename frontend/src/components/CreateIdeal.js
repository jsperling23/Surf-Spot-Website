import React from 'react';
import {  useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';


function CreateIdeal() {
    const location = useLocation();
    const spotID = location.state?.spotID;
    const navigate = useNavigate();
    const [windDir, setWind] = useState(null);
    const [swellDir, setSwell] = useState(null);
    const [size, setSize] = useState(null);
    const [period, setPeriod] = useState(null);
    const [tideMin, setMin] = useState(null);
    const [tideMax, setMax] = useState(null);

    console.log("spotID: ", spotID)
    async function handleSubmit(e){
        e.preventDefault();
        const send = {
            "spotID": spotID,
            "windDir": windDir,
            "swellDir": swellDir,
            "size": size,
            "period": period,
            "tideMin": tideMin,
            "tideMax": tideMax
        };
        console.log(send)
        const createIdeal = await fetch("/backend/ideal",
            {method: 'POST',
            headers: {
                'Content-Type': 'application/json'},
            body: JSON.stringify({
                    spotID: spotID,
                    windDir: windDir,
                    swellDir: swellDir,
                    size: size,
                    period: period,
                    tideMin: tideMin,
                    tideMax: tideMax
                }),
            credentials: 'include'
            });
            if (createIdeal.status === 201) {
                const response = await createIdeal.json()
                console.log(response)
                alert("Ideal Conditions Saved")
                navigate('/');
            } else {
                const responseData = await createIdeal.json();
                console.log(responseData)
                alert(responseData.result)
            };
    };

    return(
        <>
            <form onSubmit={ handleSubmit }>
                <fieldset>
                    <legend>Fill out the ideal conditions for your surf spot below</legend>
                    <label htmlFor='windDir'>Wind Direction: </label>
                    <select id='windDir' name='windDir' onChange={e => setWind(e.target.value)}>
                        <option value="" disabled selected>Select Wind Direction</option>
                        <option value="N">N</option>
                        <option value="NNW">NNW</option>
                        <option value="NW">NW</option>
                        <option value="WNW">WNW</option>
                        <option value="SW">SW</option>
                        <option value="SSW">SSW</option>
                        <option value="S">S</option>
                        <option value="SSE">SSE</option>
                        <option value="SE">SE</option>
                        <option value="E">E</option>
                        <option value="NE">NE</option>
                        <option value="NNE">NNE</option>
                    </select>
                    <br></br>
                    <label htmlFor='swellDir'>Swell Direction: </label>
                    <select id='swellDir' name='swellDir' onChange={e => setSwell(e.target.value)}>
                        <option value="" disabled selected>Select Swell Direction</option>
                        <option value="N">N</option>
                        <option value="NNW">NNW</option>
                        <option value="NW">NW</option>
                        <option value="WNW">WNW</option>
                        <option value="W">W</option>
                        <option value="WSW">W</option>
                        <option value="SW">SW</option>
                        <option value="SSW">SSW</option>
                        <option value="S">S</option>
                        <option value="SSE">SSE</option>
                        <option value="SE">SE</option>
                        <option value="E">E</option>
                        <option value="NE">NE</option>
                        <option value="NNE">NNE</option>
                    </select>
                    <br></br>
                    <label htmlFor='size' >Size: </label>
                    <select id='size' name='size' onChange={e => setSize(e.target.value)}>
                        <option value="" disabled selected>Select Size</option>
                        <option value="Waist High">Waist High</option>
                        <option value="Shoulder High">Shoulder High</option>
                        <option value="Head High">Head High</option>
                        <option value="Overhead">Overhead</option>
                        <option value="Double Overhead">Double Overhead</option>
                        <option value="Triple Overhead">Triple Overhead</option>
                        <option value="Waist High+">Waist High+</option>
                        <option value="Shoulder High+">Shoulder High+</option>
                        <option value="Head High+">Head High+</option>
                        <option value="Overhead+">Overhead+</option>
                    </select>
                    <br></br>
                    <label htmlFor='period' >Period: </label>
                    <select id='period' name='period' onChange={e => setPeriod(e.target.value)}>
                        <option value="" disabled selected>Select Period</option>
                        <option value="Short(<9s)">short(&lt;9s)</option>
                        <option value="Medium(10-14s)">Medium(10-14s)</option>
                        <option value="Long(15s+)">Long(15s+)</option>
                    </select>
                    <br></br>
                    <label htmlFor='tideMin'>Minimum Tide: </label>
                    <input
                    type='decimal'
                    maxLength='4'
                    placeholder='ex. 2.3'
                    onChange={e => setMin(e.target.value)}>
                    </input>
                    <br></br>
                    <label htmlFor='tideMax'>Maximum Tide: </label>
                    <input
                    type='decimal'
                    maxLength='4'
                    placeholder='ex. 5.0'
                    onChange={e => setMax(e.target.value)}>
                    </input>
                    <br></br>
                    <br></br>
                    <button type='submit'>Submit</button>
                </fieldset>
            </form>
        </>
    )
};

export default CreateIdeal