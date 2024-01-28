import React from "react";
import { Outlet, Navigate } from "react-router-dom";
import { useAuthContext } from "../authContext";

export default function ProtectedRouter() {
  const { isAuthenticated } = useAuthContext();

  if (!isAuthenticated) {
    return <Navigate to={"/"} />;
  }

  return (
    <div>
      <Outlet />
    </div>
  );
}
