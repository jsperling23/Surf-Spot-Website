import React from 'react'; 
import {  useState } from 'react';
import { useNavigate } from 'react-router-dom';

//login function
async function loginFunc(username, password) {
    const login = await fetch(`http://localhost:5000/login`,
        {method: 'POST',
        headers: {
            'Content-Type': 'application/json'},
        body: JSON.stringify({
                username: username,
                password: password
            }),
        credentials: 'include'
        }
    );
    console.log(login.headers);
    return login.status
};



function Login() {
    const [loggedStatus, setStatus] = useState(false);
    const [username, setUsername] = useState(null);
    const [password, setPassword] = useState(null);
    const [failed, setFailed] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const login = await loginFunc(username, password)
        if (login === 200) {
            console.log(login, loggedStatus)
            setStatus(true);
            console.log(loggedStatus)
            navigate('/');
        } else {
            setFailed(true)
            alert('Incorrect username or passord')
        }
    };
    

    return (
        <div>
            <header className='loginHeader'>Log in</header>
            <div className="loginContainer">
                <form onSubmit={ handleSubmit }>
                    <fieldset>
                        <legend>Please enter your username and password</legend>
                        <label htmlFor='username'>Username: </label>
                        <input
                        className='username'
                        type='text'
                        required
                        maxLength='100'
                        placeholder='ex. KrustyKrab'
                        onChange={e => setUsername(e.target.value)}
                        autoFocus
                        >
                        </input>
                        <br></br>
                        <br></br>
                        <label htmlFor='password'>Password: </label>
                        <input
                        className='password'
                        type='password'
                        required
                        maxLength='100'
                        onChange={e => setPassword(e.target.value)}
                        >
                        </input>
                        <br></br>
                        <br></br>
                        <button type='submit'>Log in</button>
                    </fieldset>
                </form>
                {failed? (
                    <p>Don't have an account? Create one here!</p>
                ) : null}
            </div>
        </div>
    )
};

export default Login;