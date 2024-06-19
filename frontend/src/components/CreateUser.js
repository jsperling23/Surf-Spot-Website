import React from 'react'; 
import {  useState } from 'react';
import { useNavigate } from 'react-router-dom';

function CreateUser () {
    const [username, setUsername] = useState(null);
    const [password, setPassword] = useState(null);
    const [password2, setPassword2] = useState(null);
    const navigate = useNavigate();

    async function createFunc(username, password) {
        const create = await fetch(`/createUser`,
            {method: 'POST',
            headers: {
                'Content-Type': 'application/json'},
                body: JSON.stringify({
                    username: username,
                    password: password
                }), credentials: 'include'
            }
        );
        console.log(create.headers);
        return create
    };
    
    // deal with form submission
    const handleSubmit = async (e) => {
        if (password != password2) {
            return alert('Passwords do not match')
        };
        e.preventDefault();
        const create = await createFunc(username, password)
        if (create.status === 200) {
            console.log(create.status)
            alert("Account creation successful")
            navigate('/');
        } else {
            const responseData = await create.json();
            console.log(responseData)
            alert(responseData.result)
        };
    };



    return (
        <div>
            <header className='loginHeader'>Create account below</header>
            <div className="loginContainer">
                <form onSubmit={ handleSubmit }>
                    <fieldset>
                        <legend>Please enter your desired username and password</legend>
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
                        <label htmlFor='password'>Re-enter Password: </label>
                        <input
                        className='password'
                        type='password'
                        required
                        maxLength='100'
                        onChange={e => setPassword2(e.target.value)}
                        >
                        </input>
                        <br></br>
                        <br></br>
                        <button type='submit'>Log in</button>
                    </fieldset>
                </form>
            </div>
        </div>
    )
}

export default CreateUser;