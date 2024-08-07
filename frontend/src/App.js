import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Homepage from './components/Homepage';
import Buoy from './components/buoy';
import CreateUser from './components/CreateUser';
import Login from './components/Login';
import CreateSpot from './components/CreateSpot';
import CreateIdeal from './components/CreateIdeal';
import CreateSession from './components/CreateSession';

function App() {
  return (
    <>
      <BrowserRouter>
        <header className = "top">My Surf Journal</header>
        <main>
          <section>
            <Routes>
              <Route path = "/createSession" element = { <CreateSession/> } />
              <Route path = "/createIdeal" element = { <CreateIdeal /> }/> 
              <Route path = "/createSpot" element = { <CreateSpot /> }/>
              <Route path = "/login" element = { <Login /> } />
              <Route path = "/" element = { <Homepage /> }/>
              <Route path = "/buoyDisplay" element = { <Buoy />}/>
              <Route path = "/CreateUser" element = { <CreateUser />} />
            </Routes>
          </section>
        </main>
      </BrowserRouter>
    </>
  );
}

export default App;
