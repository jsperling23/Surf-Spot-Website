import React from 'react';
import { useLocation, NavLink } from 'react-router-dom';
import {  useState, useEffect } from 'react';


//Main component of this page
function Buoy () {
    const location = useLocation()
    const [buoyData, setData] = useState(null)
    const [units, setUnits] = useState("imperial")
    const [prevUnits, setPrevUnits] = useState(units)
    const [height, setHeight] = useState(null)
    const [heightUnit, setHeightUnit] = useState("Feet")
    const [windUnit, setWindUnit] = useState("MPH")
    const [waterUnit, setWaterUnit] = useState("°F")
    const [water, setWater] = useState(null)
    const [wind, setWind] = useState(null)
    const buoyId = location.state?.buoy

    //Function to fetch the buoy data
    async function getBuoyData (stationID) {
      const response = await fetch(`http://localhost:5000/request?stationID=${stationID}`)
      const data = await response.json()
      return JSON.parse(data)
    }; 

    //Call the getBuoyData function and set the state of buoyData
    useEffect(() => {
        async function fetchData() {
            try{
                if (buoyId) {
                  const response = await getBuoyData(buoyId);
                  setData(response);
                  console.log("its called and data is set")
                  if (!isNaN(response.WVHT)) {
                    setHeight((response.WVHT * 3.28084).toFixed(2))
                  } else{setHeight(response.WVHT)};

                  if (!isNaN(response.WTMP)) {
                    setWater((response.WTMP * 1.8 + 32).toFixed(2))
                  } else{setWater(response.WTMP)};

                  if (!isNaN(response.WSPD)) {
                    setWind((response.WSPD * 2.23694).toFixed(2))
                  }else {setWind(response.WSPD)};
                }
            
            }
            catch(error){
                console.error("The following error has occurred: ", error)
            }
        }
        if (buoyId) {
        fetchData()};
    }, [buoyId])


    //Handle swapping units
    const handleUnitChange = (event) => {
      setPrevUnits((prevUnits) => {
        const newUnits = event.target.value;
        setUnits(newUnits);

        if (newUnits === "imperial") {

          //Deal with numbers 
          setHeightUnit("Feet");
          setWaterUnit("°F");
          setWindUnit("MPH");

          //Deal with numbers
          if (!isNaN(height)) {
            setHeight((height * 3.28084).toFixed(2))
          };

          if (!isNaN(water)) {
            setWater((water * 1.8 + 32).toFixed(2))
          };
          
          
          if (!isNaN(wind)) {
            setWind((wind * 2.23694).toFixed(2))
          };
        } else {

          //Deal with units 
          setHeightUnit("Meters");
          setWaterUnit("°C");
          setWindUnit("M/S");

          //Deal with actual numbers
          if (!isNaN(height)) {
            setHeight((height * 0.3048).toFixed(2))
          };

          if (!isNaN(water)) {
            setWater(((water - 32) * 5/9).toFixed(2))
          };
          
          if (!isNaN(wind)) {
            setWind((wind * 0.44704).toFixed(2))
          };
        }

        return prevUnits;
      });
    };

    
    
    //HTML to be returned by function, depends on if the fetch promise returned 
    return (
        <div>
          <header class="buoyHeader">Current Data For Station {buoyId}</header>
          {buoyData ? ( 
            <div class="buoyData">
              <table >
                <thead>
                  <tr>
                    <th>Parameter</th>
                    <th>Data</th>
                    <th>Unit</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Wave Height</td>
                    <td>{ height }</td>
                    <td>{ heightUnit }</td>
                  </tr>
                  <tr>
                    <td>Period</td>
                    <td>{ buoyData.DPD }</td>
                    <td>Seconds</td>
                  </tr>
                  <tr>
                    <td>Swell Direction</td>
                    <td>{ buoyData.MWD }</td>
                    <td>Degrees</td>
                  </tr>
                  <tr>
                    <td>Wind Speed</td>
                    <td>{ wind }</td>
                    <td>{ windUnit }</td>
                  </tr>
                  <tr>
                    <td>Wind Direction</td>
                    <td>{ buoyData.WDIR }</td>
                    <td>Degrees</td>
                  </tr>
                  <tr>
                    <td>Water Temperature</td>
                    <td>{ water }</td>
                    <td>{ waterUnit }</td>
                  </tr>
                </tbody>
              </table>
              <input type="radio" id="imperial" checked={units === "imperial"} onChange={handleUnitChange} name="units" value="imperial"/>
              <label htmlFor="html">Imperial</label><br/>
              <input type="radio" id="metric" checked={units === "metric"} onChange={handleUnitChange} name="units" value="metric"/>
              <label htmlFor="html">Metric</label>
              <p>MM indicates that the buoy does not collect that information<br/>Click the naviation link below to try again</p>
            </div>
          ) : (
            <p>Loading...</p>
          )}
          <NavLink to="/">Return Home</NavLink>
        </div>
      );   
}

export default Buoy