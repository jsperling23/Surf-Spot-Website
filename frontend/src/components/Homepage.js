import { useState, useEffect } from 'react';
import { useNavigate, NavLink } from 'react-router-dom';
import LoggedHome from './loggedHome';
import NotLoggedHome from './notLoggedHome';
import Menu from './Menu';



function Homepage() {
    console.log("component rendered")

    const [loggedStatus, setStatus] = useState(null);

    //If user is logged in, continue, else, redirect to the login page
    const checkAuth = async () => {
        const auth = await fetch(`/backend/auth`, {credentials: 'include'});
        if (auth.status === 200) {
            setStatus(true)
        } else { setStatus(false) };
    };
    
    useEffect(() => {
        checkAuth()
    }, [])

    const handleLogout = () => {
        setStatus(false)
    }
    
    return (
        <>
            { (loggedStatus != null) ?
            <div classname="homepage">
                <div className='Menu'>{ <Menu onClick = { handleLogout } logged = { loggedStatus }/> }</div>
                <div>{ loggedStatus ? <LoggedHome/> : <NotLoggedHome/>}</div>
            </div>
            : <div>...loading</div>}
            
        </>
    )
};

export default Homepage