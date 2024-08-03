import React from 'react';
import { useState, useEffect } from 'react';


function Session({ session, updateSessions, handleUpdate }) {
    const [collapse, setCollapse] = useState(false);
    const [edit, setEdit] = useState(false);
    let editData = JSON.parse(JSON.stringify(session))
    const sessionID = session.sessionID;

    async function handleDelete(e) {
        e.preventDefault();
        const decision = window.confirm("Are you sure you want to delete this spot?");
        if (!decision) return;
        const deleteSpot = await fetch(`/backend/Sessions?sessionID=${sessionID}`,
            {method: 'DELETE', credentials: 'include'});
            if (deleteSpot.status === 201) {
                const response = await deleteSpot.json()
                console.log(response);
                updateSessions(sessionID);
            } else {
                const responseData = await deleteSpot.json();
                console.log(responseData)
                alert(responseData.result)
            };
    };

    async function handleEdit(e) {
        e.preventDefault();
        console.log("edit request data: ", editData)
        const editSesh = await fetch("/backend/Sessions",
            {method: 'PUT',
            headers: {
                'Content-Type': 'application/json'},
            body: JSON.stringify({
                spotID: editData.spotID,
                sessionID: editData.sessionID,
                date: new Date(editData.date).toISOString().substring(0, 10),
                windSpd: editData.windSpeed,
                windDir: editData.windDirection,
                swellHgt: editData.swellHeight,
                swellPer: editData.swellPeriod,
                swellDir: editData.swellDirection,
                tide: editData.tide,
                swellAct: editData.swellActivity,
                tideDir: editData.tideDirecton,
                description: editData.description
                }),
            credentials: 'include'
            });
        
        if (editSesh.status === 201) {
            const response = await editSesh.json()
            console.log(response)
            handleUpdate(editData)
        } else {
            const responseData = await editSesh.json();
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
            <table className="surfSpotTable">
                <tbody>
                    <tr>
                    <td>{session.date.split(" ").slice(0, 4).join(" ")}</td>
                    <td className="surfExpand" colSpan='5'>
                        <button onClick={() => { setCollapse(!collapse) }}> + </button>
                    </td>
                    </tr>
                    {collapse ?
                    <>
                        <tr>
                            <td><strong>Spot Name: </strong>{ session.name }</td>
                            <td><strong>Wind Speed(mph): </strong>{ session.windSpeed }</td>
                            <td><strong>Wind Direction(°): </strong>{ session.windDirection }</td>
                        </tr>
                        <tr>
                            <td><strong>Swell Height(ft): </strong>{ session.swellHeight }</td>
                            <td><strong>Swell Period(s): </strong>{ session.swellPeriod }</td>
                            <td><strong>Swell Direction(°): </strong>{ session.swellDirection }</td>
                        </tr>
                        <tr>
                            <td><strong>Tide(ft): </strong>{ session.tide }</td>
                            <td><strong>Swell Activity: </strong>{ session.swellActivity }</td>
                            <td><strong>Tide Direction: </strong>{ session.tideDirecton }</td>
                        </tr>
                        <tr>
                            <td colSpan='5'><strong>Description: </strong>{ session.description }</td>
                        </tr>
                        <tr>
                            <td colSpan='5'> 
                                <button onClick = { handleDelete }> Delete Session </button>
                                <button onClick = {() => { setEdit(true) }}> Edit Session </button>
                            </td>
                        </tr>
                    </> : <></>
                    }
            </tbody>
            </table> :
            <form onSubmit={ handleEdit }>
                <table className="surfSpotTable">
                    <tbody>
                        <tr>
                        <td>
                            <input
                            type='date'
                            placeholder='ex. 4/20/2024'
                            defaultValue={new Date(editData.date).toISOString().substring(0, 10)}
                            onChange={ e => editData.date = e.target.value}>
                            </input>
                        </td>
                        </tr>
                        <>
                            <tr>
                                <td><strong>Spot Name: </strong>{ session.name }</td>
                                <td><strong>Wind Speed(mph): </strong>
                                    <input
                                    type='decimal'
                                    placeholder='4'
                                    defaultValue={ editData.windSpeed }
                                    onChange={e => editData.windSpeed = e.target.value}>
                                    </input>
                                </td>
                                <td><strong>Wind Direction(°): </strong>
                                    <input
                                    type='decimal'
                                    placeholder='4'
                                    defaultValue={ editData.windDirection }
                                    onChange={e => editData.windDirection = e.target.value}>
                                    </input>
                                </td>
                            </tr>
                            <tr>
                            <   td><strong>Swell Height(ft): </strong>
                                    <input
                                    type='decimal'
                                    placeholder='4'
                                    defaultValue={ editData.swellHeight}
                                    onChange={e => editData.swellHeight = e.target.value}>
                                    </input>
                                </td>
                                <td><strong>Swell Period(s): </strong>
                                    <input
                                    type='number'
                                    placeholder='4'
                                    defaultValue={ editData.swellPeriod }
                                    onChange={e => editData.swellPeriod = e.target.value }>
                                    </input> 
                                </td>
                                <td><strong>Swell Direction(°): </strong>
                                    <input
                                    type='number'
                                    placeholder='ex. 270'
                                    defaultValue={ editData.swellDirection }
                                    onChange={e => editData.swellDirection = e.target.value }>
                                    </input>
                                </td>
                            </tr>
                            <tr>
                                <td><strong>Tide(ft): </strong>
                                    <input
                                    type='number'
                                    placeholder='4'
                                    defaultValue={ editData.tide }
                                    onChange={e => editData.tide = e.target.value}>
                                    </input>
                                </td>
                                <td><strong>Swell Activity: </strong>
                                    <select id='swellAct' name='swellAct' onChange={e => editData.swellActivity = e.target.value}>
                                        <option value={editData.swellActivity} >{ editData.swellActivity }</option>
                                        <option value="Increasing">Increasing</option>
                                        <option value="Decreasing">Decreasing</option>
                                        <option value="Steady">Steady</option>
                                    </select>
                                </td>
                                <td><strong>Tide Direction: </strong>
                                    <select id='tideDir' name='tideDir' onChange={e => editData.tideDirecton = e.target.value}>
                                        <option value={editData.tideDirecton} >{ editData.tideDirecton }</option>
                                        <option value="Increasing">Increasing</option>
                                        <option value="Decreasing">Decreasing</option>
                                        <option value="Slack">Slack</option>
                                    </select>
                                </td>
                            </tr>
                            <tr>
                                <td colSpan='4'><strong>Description: </strong>
                                    <textarea
                                    placeholder='Write about your sesh...'
                                    defaultValue={editData.description}
                                    onChange={e => editData.description = e.target.value}
                                    style={{ width: '90%', height: '100px', fontSize: '16px', resize: 'none' }}
                                    />
                                </td>
                            </tr>
                            <tr>
                                <td colSpan='5'> 
                                    <button onClick = { handleCancel }> Cancel </button>
                                    <button type='submit'>Save</button>
                                </td>
                            </tr>
                        </>
                </tbody>
                </table>
            </form>
            }
            
      </>
    )
    }

function Sessions() {

    const [seshData, setData] = useState(null);
    const [user, setUser] = useState(null);

    // Get all surf sessions for a specific userID
    async function getSessions(user) {
        const response = await (fetch(`/backend/Sessions?userID=${user}`,
          { method: "GET" }))
        const data = await response.json()
        return data
      };

    
    function handleUpdate(data) {
        setData(() => {
            const updated = {...seshData};
            updated[data.sessionID] = data
            return updated
        })
        console.log("After update: ", seshData)
    };


    useEffect(() => {
        const userID = sessionStorage.getItem("userID");
        if (userID) {
          setUser(userID);
          console.log(userID);
        }

    }, []);

    useEffect(() => {
        async function fetchData() {
            try {
            const data = await getSessions(user)
            setData(data)
            console.log(data)
            } catch (error) {
            console.error(error)
            };

        };
        if (user) {
            fetchData()
        };
        }, [user]);

    function updateSessions(id) {
        setData(() => {
            const updated = {...seshData};
            console.log("Now deleted: ", updated[id])
            delete updated[id]
            return updated
        })
    };

    return (
      <>
        <div>
          <legend><strong>My Sessions</strong></legend>
            {
                seshData ?
                    Object.keys(seshData).length > 0 ? 
                    (Object.values(seshData).map((session) => (
                        <Session
                            handleUpdate={handleUpdate}
                            updateSessions={updateSessions}
                            session={session}
                            key={session.sessionID}
                        />
                ))) : <p>No Sessions Saved</p> :
                <p>...Loading</p>
            }
        </div>
      </>
    )
  };



export default Sessions;