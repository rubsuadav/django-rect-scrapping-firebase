import React from "react";
import { Outlet } from "react-router-dom";

export default function PublicRouter() {
  return (
    <div>
      <Outlet />
    </div>
  );
}
