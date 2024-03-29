import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// local layout imports
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

// local pages imports
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import Home from "./pages/Home";
import Chat from "./pages/Chat";

// Authentication and routers imports
import { AuthContextProvider } from "./context/authContext";
import PublicRouter from "./context/routers/PublicRouter";
import PrivateRouter from "./context/routers/PrivateRouter";
import ProtectedRouter from "./context/routers/ProtectedRouter";

export default function App() {
  return (
    <div>
      <AuthContextProvider>
        <Router>
          <Navbar />
          <Routes>
            {/* Public routes  =====================================*/}
            <Route path="/" element={<PublicRouter />}>
              <Route index element={<Home />} />
            </Route>
            {/* Login and register */}
            <Route path="" element={<PrivateRouter />}>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
            </Route>
            {/* Protected routes  =====================================*/}
            <Route path="" element={<ProtectedRouter />}>
              <Route path="/chat" element={<Chat />} />
            </Route>
          </Routes>
          <Footer />
        </Router>
      </AuthContextProvider>
    </div>
  );
}
