import React from 'react';
import {  useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function CreateSession() {
    const [spot, setSpot] = useState(null);
    const [date, setDate] = useState(null);
    const [windSpd, setWindSpd] = useState(null);
    const [windDir, setWindDir] = useState(null);
    const [swellHgt, setHgt] = useState(null);
    const [swellPer, setPer] = useState(null);
    const [swellDir, setDir] = useState(null);
    const [tide, setTide] = useState(null);
    const [swellAct, setSwellAct] = useState(null);
    const [tideDir, setTideDir] = useState(null);
    const [description, setDescription] = useState(null);
    const location = useLocation();
    const spotData = location.state.spotData
    const navigate = useNavigate();
    async function handleSubmit(e) {
        e.preventDefault();

        const saveSesh = await fetch("/Sessions",
            {method: 'POST',
            headers: {
                'Content-Type': 'application/json'},
            body: JSON.stringify({
                    spotID: spot,
                    date: date,
                    windSpd: windSpd,
                    windDir: windDir,
                    swellHgt: swellHgt,
                    swellPer:swellPer,
                    swellDir: swellDir,
                    tide: tide,
                    swellAct: swellAct,
                    tideDir: tideDir,
                    description: description
                }),
            credentials: 'include'
            });
        if (saveSesh.status === 201) {
            const response = await saveSesh.json()
            console.log(response)
        } else {
            const responseData = await saveSesh.json();
            console.log(responseData)
            alert(responseData.result)
        };
        navigate('/')
        return
    };

    return(
        <>
        
             { spotData ? <form onSubmit={ handleSubmit }>
                <fieldset>
                    <legend>Fill out the ideal conditions for your surf spot below</legend>
                    <label htmlFor="name">Choose the Spot: </label>
                    <select id='name' name='name' onChange={e => setSpot(e.target.value)}>
                        {Object.values(spotData).map((session) => (
                            <option key={session.spotID} value={session.spotID}>{session.name}</option>    
                        ))}
                    </select>
                    <br></br>
                    <label htmlFor="date">Enter Date: </label>
                    <input
                    type='date'
                    placeholder='ex. 4/20/2024'
                    onChange={e => setDate(e.target.value)}>
                    </input>
                    <br></br>
                    <label htmlFor="windSpd">Enter WindSpeed(mph): </label>
                    <input
                    type='decimal'
                    placeholder='4'
                    onChange={e => setWindSpd(e.target.value)}>
                    </input>
                    <br></br>
                    <label htmlFor="windDir">Enter Wind Direction(degrees): </label>
                    <input
                    type='decimal'
                    placeholder='4'
                    onChange={e => setWindDir(e.target.value)}>
                    </input>
                    <br></br>
                    <label htmlFor="swellHgt">Swell Height(ft): </label>
                    <input
                    type='decimal'
                    placeholder='4'
                    onChange={e => setHgt(e.target.value)}>
                    </input>
                    <br></br>
                    <label htmlFor="swellPer">Swell Period(s): </label>
                    <input
                    type='number'
                    placeholder='4'
                    onChange={e => setPer(e.target.value)}>
                    </input>
                    <br></br>
                    <label htmlFor="swellDir">Swell Direction(degrees): </label>
                    <input
                    type='number'
                    placeholder='ex. 270'
                    onChange={e => setDir(e.target.value)}>
                    </input>
                    <br></br>
                    <label htmlFor="tide">Tide(ft): </label>
                    <input
                    type='number'
                    placeholder='4'
                    onChange={e => setTide(e.target.value)}>
                    </input>
                    <br></br>
                    <label htmlFor="swellAct">Swell Activity: </label>
                    <select id='swellActu' name='swellDir' onChange={e => setSwellAct(e.target.value)} defaultValue="">
                        <option value="" disabled>Select Swell Activity</option>
                        <option value="Increasing">Increasing</option>
                        <option value="Decreasing">Decreasing</option>
                        <option value="Slack">Steady</option>
                    </select>
                    <br></br>
                    <label htmlFor="tideDir">Tide Direction: </label>
                    <select id='tideDir' name='tideDir' onChange={e => setTideDir(e.target.value)} defaultValue="">
                        <option value="" disabled>Select Tide Direction</option>
                        <option value="Increasing">Increasing</option>
                        <option value="Decreasing">Decreasing</option>
                        <option value="Slack">Slack</option>
                    </select>
                    <br></br>
                    <label htmlFor="description">Notes: </label>
                    <input
                    type='text'
                    placeholder='Write about your sesh...'
                    onChange={e => setDescription(e.target.value)}>
                    </input>
                    <br></br>
                    <br></br>
                    <button type='submit'>Submit</button>
                </fieldset>
            </form> : <p>...Loading</p>}
        </>
    )
};

export default CreateSession