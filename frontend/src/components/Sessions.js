import React from 'react';
import { useState, useEffect } from 'react';


function Session({ session, updateSessions }) {
    const [collapse, setCollapse] = useState(false)
    const sessionID = session["sessionID"]

    async function handleDelete(e) {
        e.preventDefault();
        const decision = window.confirm("Are you sure you want to delete this spot?");
        if (!decision) return;
        const deleteSpot = await fetch(`/Sessions?sessionID=${sessionID}`,
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

    return (
      <>
          <table className="surfSpotTable">
              <tbody>
                  <tr>
                    <td> {session["date"].split(" ").slice(0, 4).join(" ")}</td>
                    <td className="surfExpand" colSpan='5'>
                      <button onClick={() => { setCollapse(!collapse) }}> + </button>
                    </td>
                  </tr>
                  {collapse ?
                    <>
                        <tr>
                            <td><strong>Spot Name: </strong>{ session["name"] }</td>
                            <td><strong>Wind Speed: </strong>{ session["windSpeed"] }</td>
                            <td><strong>Wind Direction: </strong>{ session["windDirection"] }</td>
                            <td><strong>Swell Height: </strong>{ session["swellHeight"] }</td>
                            <td><strong>Swell Period(s): </strong>{ session["swellPeriod"] }</td>
                            
                        </tr>
                        <tr>
                            <td><strong>Swell Direction: </strong>{ session["swellDirection"] }</td>
                            <td><strong>Tide: </strong>{ session["tide"] }</td>
                            <td><strong>Swell Activity: </strong>{ session["swellActivity"] }</td>
                            <td><strong>Tide Direction: </strong>{ session["tideDirecton"] }</td>
                        </tr>
                        <tr>
                            <td><strong>Description: </strong>{ session["description"] }</td>
                        </tr>
                        <tr>
                            <td colSpan='5'> 
                                <button onClick = { handleDelete }> Delete Spot </button>
                            </td>
                        </tr>
                    </> : <></>
                  }
            </tbody>
        </table>
      </>
    )
    }

function Sessions() {

    const [seshData, setData] = useState(null);
    const [user, setUser] = useState(null);

    // Get all surf sessions for a specific userID
    async function getSessions(user) {
        const response = await (fetch(`/Sessions?userID=${user}`,
          { method: "GET" }))
        const data = await response.json()
        return data
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
          <legend>My Sessions</legend>
          {
            seshData ?
              Object.values(seshData).map((session, key) => (
                <Session
                  updateSessions={updateSessions}
                  session={session}
                  key={key}
                />
              )) :
              <p>...Loading</p>
          }
        </div>
      </>
    )
  };



export default Sessions;