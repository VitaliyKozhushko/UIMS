import React from "react";
import {Navigate, Outlet} from "react-router-dom";

interface ProtectedRouteProps {}

function ProtectedRoute(props: ProtectedRouteProps) {
  const loginTime = localStorage.getItem('loginTime');
  const maxTime = 15 * 60 * 1000;

  if (loginTime) {
    const currentTime = new Date().getTime();
    const timeDiff = currentTime - parseInt(loginTime, 10);

    if (timeDiff < maxTime) {
      return <Outlet/>;
    } else {
      localStorage.removeItem('loginTime');
      return <Navigate to="/"/>;
    }
  }

  return <Navigate to="/"/>;
}

export default ProtectedRoute;
