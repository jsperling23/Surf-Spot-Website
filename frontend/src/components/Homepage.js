import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import LoggedHome from './loggedHome';
import NotLoggedHome from './notLoggedHome';
import Menu from './LoggedNav';



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
            <div>{ loggedStatus ? <Menu onClick = { handleLogout }/> : null}</div>
            <div>{ loggedStatus ? <LoggedHome/> : <NotLoggedHome/>}</div>
        </>
    )
};

export default Homepage