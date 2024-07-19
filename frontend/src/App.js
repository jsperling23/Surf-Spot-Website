import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Homepage from './components/Homepage';
import Buoy from './components/buoy';
import CreateUser from './components/CreateUser';
import Login from './components/Login';
import CreateSpot from './components/CreateSpot'

function App() {
  return (
    <>
      <BrowserRouter>
        <header className = "top">Buoy Data Finder</header>
        <main>
          <section>
            <Routes>

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
