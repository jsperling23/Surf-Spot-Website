import React from 'react';
import {  useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import HomeMap from './HomeMap'


function Spot( { surfSpot, updateSpots, handleUpdate } ) {
    const [collapse, setCollapse] = useState(false)
    const [edit, setEdit] = useState(false)
    let editData = JSON.parse(JSON.stringify(surfSpot))
    const spotID = surfSpot["spotID"]
    console.log(surfSpot)

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

    async function handleEdit(e) {
        e.preventDefault();
        const editSpot = await fetch("/surfSpot",
            {method: 'PUT',
            headers: {
                'Content-Type': 'application/json'},
            body: JSON.stringify({
                    spotID: editData.spotID,
                    name: editData.name,
                    latitude: editData.latitude,
                    longitude: editData.longitude,
                    firstStation: editData.buoy1,
                    secondStation: editData.buoy2,
                    windDir: editData.ideal.windDir,
                    swellDir: editData.ideal.swellDir,
                    size: editData.ideal.waveSize,
                    period: editData.ideal.period,
                    tideMin: editData.ideal.tideMin,
                    tideMax: editData.ideal.tideMax
                }),
            credentials: 'include'
            });
        
        if (editSpot.status === 201) {
            const response = await editSpot.json()
            console.log(response)
            handleUpdate(editData)
        } else {
            const responseData = await editSpot.json();
            console.log(responseData)
            alert(responseData.result)
        };
        
        setEdit(false)
    };

    function handleCancel() {
        setEdit(false) 
    };

    return (
        <>
            {!edit ? 
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
                                <td colSpan='2'> 
                                    <button onClick = { handleDelete }> Delete Spot </button>
                                </td>
                                <td colSpan='2'> 
                                    <button onClick = {() => { setEdit(true) }}> Edit Spot </button>
                                </td>
                            </tr>   
                        </> : <></>
                        }
                </tbody>     
            </table> :  
            <form onSubmit = { handleCancel }>
                <table className = "surfEditTable">
                <tbody>
                        <tr>
                            <td><label htmlFor='spotName'>Name: </label>
                                <input
                                type='text'
                                required
                                maxLength='100'
                                placeholder="ex. Pipeline"
                                defaultValue={editData["name"]}
                                onChange={e => editData["name"] = e.target.value}>
                                </input></td>
                            <td className = "surfExpand" colSpan='5'> 
                                <button onClick = {() => {setCollapse(!collapse)}}> + </button>
                            </td>
                        </tr>
                            <tr>
                                <td>Buoy 1:</td>
                                <td><input
                                    type='text'
                                    maxLength='10'
                                    defaultValue={editData["buoy1"]}
                                    onChange={e => editData["buoy1"] = e.target.value}>
                                    </input>
                                </td>
                            </tr>
                            <tr>
                                <td>Buoy 2:</td>
                                <td><input
                                    type='text'
                                    maxLength='10'
                                    defaultValue={editData["buoy2"]}
                                    onChange={e => editData["buoy2"] = e.target.value}>
                                    </input>
                                </td>
                            </tr> 
                            <tr>
                                <td><strong>Ideal Period: </strong> 
                                    <select id='windDir' name='windDir' onChange={e => editData["ideal"]["period"] = e.target.value}>
                                        <option value={editData["ideal"]["period"]}>{editData["ideal"]["period"]}</option>
                                        <option value="Short(<9s)">short(&lt;9s)</option>
                                        <option value="Medium(10-14s)">Medium(10-14s)</option>
                                        <option value="Long(15s+)">Long(15s+)</option>    
                                    </select></td>
                                <td><strong>Ideal Swell Direction: </strong>
                                    <select id='swellDir' name='swellDir' onChange={e => editData["ideal"]["swellDir"] = e.target.value}>
                                        <option value={surfSpot["ideal"]["swellDir"]}>{editData["ideal"]["swellDir"]}</option>
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
                                </td>
                            </tr>
                            <tr>
                                <td><strong>Max Tide: </strong>
                                        <input
                                        type='decimal'
                                        maxLength='4'
                                        placeholder='ex. 2.3'
                                        defaultValue={editData["ideal"]["tideMax"]}
                                        onChange={e => editData["ideal"]["tideMax"] = e.target.value}>
                                        </input>
                                    </td>
                                    <td><strong>Min Tide: </strong>
                                        <input
                                        type='decimal'
                                        maxLength='4'
                                        placeholder='ex. 2.3'
                                        defaultValue={editData["ideal"]["tideMin"]}
                                        onChange={e => editData["ideal"]["tideMin"] = e.target.value}>
                                        </input>
                                    </td>
                                    <td><strong>Ideal Size: </strong>
                                        <select id='size' name='size' onChange={e => editData["ideal"]["waveSize"] = e.target.value}>
                                            <option value={editData["ideal"]["waveSize"]}>{editData["ideal"]["waveSize"]}</option>
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
                                    </td>
                                    <td><strong>Ideal Wind: </strong>
                                        <select id='swellDir' name='swellDir' onChange={e => editData["ideal"]["windDir"] = e.target.value}>
                                            <option value={surfSpot["ideal"]["windDir"]}>{surfSpot["ideal"]["windDir"]}</option>
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
                                </td>
                            </tr>
                            <tr>
                                <td colSpan='2'> 
                                    <button type="submit"> cancel </button>
                                </td>
                                <td colSpan='2'> 
                                    <button onClick = { handleEdit }> Save Changes </button>
                                </td>
                            </tr> 
                </tbody>    
            </table>
            </form>
            }
        </>
    )
};

function SurfSpots() {
    const [spotData, setData] = useState(null);
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

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

    function handleUpdate(data) {
        setData(() => {
            const updated = {...spotData};
            updated[data.spotID] = data
            return updated
        })
    };

    function CreateSeshButton() {
        navigate('/createSession', {state: {spotData}})
    }
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
                console.log("spotData Request: ", data)
            } catch (error) {
                console.error(error)
            };
            
        };
        if(user) {
            fetchData()
        };
    }, [user]);

    
    return (
        
            <div>
                <HomeMap spotData = { spotData }/>             
                    <div>
                        { spotData ? 
                            Object.values(spotData).map((spot, key) => (
                                <Spot 
                                    surfSpot = { spot }
                                    key = { key }
                                    updateSpots = { updateSpots }
                                    handleUpdate = { handleUpdate }
                                />
                            )):
                            <p>...Loading</p> 
                        }
                    </div>
                    <div>
                        {spotData ?
                            <button onClick={ CreateSeshButton }>Have a good Sesh? Journal it Here!</button>
                            : <></>}
                    </div>
            </div>
        
    )
};

export default SurfSpots;
