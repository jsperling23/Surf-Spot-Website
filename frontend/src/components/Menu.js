import React from 'react';
import { NavLink } from 'react-router-dom';

function Menu( { onClick , logged }) {
  //logout function
  console.log(logged)
  const logout = async () => {
    const logout = await fetch('/logout', {
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
      <>
        <NavLink to = "/" onClick = { logout } className="nav-link" >Logout</NavLink>
        <NavLink to = "/createSpot" className="nav-link" >Create New Spot</NavLink>
      </>
    );
  } else {
    return (
      <div>
        <NavLink to = "/login" className="nav-link" >Login</NavLink>
        <NavLink to = "/CreateUser" className="nav-link" >Create Account</NavLink>
      </div>
    )
  }

}

export default Menu;
