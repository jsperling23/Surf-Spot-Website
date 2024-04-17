import React from 'react'; 
import {  useState } from 'react';
import { useNavigate } from 'react-router-dom';

function CreateUser () {
    const [username, setUsername] = useState(null);
    const [password, setPassword] = useState(null);
    const navigate = useNavigate();

    async function createFunc(username, password) {
        const create = await fetch(`http://localhost:5000/createUser`,
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
        console.log(create.headers);
        return create.status
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const create = await createFunc(username, password)
        if (create === 200) {
            alert("Account creation successful")
            //navigate('/');
        } else {
            alert('Error logging in, please try again')
        }
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
                        <button type='submit'>Log in</button>
                    </fieldset>
                </form>
            </div>
        </div>
    )
}

export default CreateUser;