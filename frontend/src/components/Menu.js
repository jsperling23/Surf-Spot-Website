import React from 'react';
import { NavLink } from 'react-router-dom';

function Menu( { onClick , logged }) {
  //logout function
  console.log(logged)
  const logout = async () => {
    const logout = await fetch('http://localhost:5000/logout', {
      method: "GET",
      credentials: 'include'
    });
    console.log(logout);
    if (logout.status === 200) {
      onClick();
    }
  };
  if (logged === true) {
    return (
      <NavLink to = "/" onClick = { logout }> Logout </NavLink>
    );
  } else {
    return (
      <div>
        <NavLink to = "/login"> Login </NavLink>
        <NavLink to = "/CreateUser"> Create Account </NavLink>
      </div>
    )
  }

}

export default Menu;
