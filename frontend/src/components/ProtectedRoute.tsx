import React, {ReactNode} from "react";
import {Navigate} from "react-router-dom";

interface ProtectedRouteProps {
  children: ReactNode;
}

function ProtectedRoute(props: ProtectedRouteProps) {
  const {children} = props

  const loginTime = localStorage.getItem('loginTime');
  const maxTime = 15 * 60 * 1000;

  if (loginTime) {
    const currentTime = new Date().getTime();
    const timeDiff = currentTime - parseInt(loginTime, 10);

    if (timeDiff < maxTime) {
      return <>{children}</>;
    } else {
      localStorage.removeItem('loginTime');
      return <Navigate to="/"/>;
    }
  }

  return <Navigate to="/"/>;
}

export default ProtectedRoute;
