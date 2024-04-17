import React from 'react';
import { NavLink } from 'react-router-dom';

function Menu( { onClick }) {
  //logout function
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

  return (
    <NavLink to = "/" onClick = { logout }> Logout </NavLink>
  );
}

export default Menu;
