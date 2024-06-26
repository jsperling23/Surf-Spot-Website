import { useState, useEffect } from 'react';
import { useNavigate, NavLink } from 'react-router-dom';
import LoggedHome from './loggedHome';
import NotLoggedHome from './notLoggedHome';
import Menu from './Menu';



function Homepage() {
    console.log("component rendered")

    const [loggedStatus, setStatus] = useState(false);
    const navigate = useNavigate();

    //If user is logged in, continue, else, redirect to the login page
    const checkAuth = async () => {
        const auth = await fetch(`http://localhost:5000/auth`, {method: 'GET', credentials: 'include'});
        if (auth.status === 200) {
            setStatus(true)
        } else {navigate('/')}
    }
    useEffect(() => {
        checkAuth()
    }, [])

    const handleLogout = () => {
        setStatus(false)
    }
    
    return (
        <>
            <div>{ <Menu onClick = { handleLogout }/> }</div>
            <div>{ loggedStatus ? <LoggedHome/> : <NotLoggedHome/>}</div>
        </>
    )
};

export default Homepage