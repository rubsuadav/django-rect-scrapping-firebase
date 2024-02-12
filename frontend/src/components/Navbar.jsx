import React from "react";
import { Link, useNavigate } from "react-router-dom";

// local imports
import { useAuthContext } from "../context/authContext";
import DropDown from "./DropDown";
import SearchRestaurant from "./SearchRestaurant";

export default function Navbar() {
  const { isAuthenticated, logout } = useAuthContext();
  let navigate = useNavigate();

  function handleLogout() {
    logout();
    localStorage.removeItem("userId");
    navigate("/");
  }

  return (
    <header className="text-white body-font bg-indigo-900">
      <div className="container mx-auto flex flex-wrap p-5 flex-col md:flex-row items-center">
        <div className="flex title-font font-medium items-center text-gray-900 mb-4 md:mb-0">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            stroke="currentColor"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            className="w-10 h-10 text-white p-2 bg-indigo-500 rounded-full"
            viewBox="0 0 24 24"
          >
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
          </svg>
          <Link to={"/"}>
            <span className="ml-3 text-xl text-white">Inicio</span>
          </Link>
        </div>
        <nav className="md:mr-auto md:ml-4 md:py-1 md:pl-4 md:border-l md:border-gray-400 flex flex-wrap items-center text-base justify-center md:space-x-10">
          <SearchRestaurant />
        </nav>
        {isAuthenticated ? (
          <div className="flex space-x-4 mt-4 md:mt-0">
            <Link
              className="inline-flex items-center bg-yellow-600 border-0 py-1 px-3 focus:outline-none hover:bg-yellow-500 rounded text-white text-xl"
              to={"/chat"}
            >
              Iniciar chat
              <svg
                fill="none"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                className="w-4 h-4 ml-1"
                viewBox="0 0 24 24"
              >
                <path d="M5 12h14M12 5l7 7-7 7"></path>
              </svg>
            </Link>
            <button
              className="inline-flex items-center bg-green-600 border-0 py-1 px-3 focus:outline-none hover:bg-green-400 rounded text-white"
              onClick={handleLogout}
            >
              Cerrar sesion
              <svg
                fill="none"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                className="w-4 h-4 ml-1"
                viewBox="0 0 24 24"
              >
                <path d="M5 12h14M12 5l7 7-7 7"></path>
              </svg>
            </button>
          </div>
        ) : (
          <div className="flex space-x-4 mt-4 md:mt-0">
            <Link
              className="inline-flex items-center bg-blue-400 border-0 py-1 px-3 focus:outline-none hover:bg-blue-500 rounded text-white"
              to={"/register"}
            >
              Registrarse
              <svg
                fill="none"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                className="w-4 h-4 ml-1"
                viewBox="0 0 24 24"
              >
                <path d="M5 12h14M12 5l7 7-7 7"></path>
              </svg>
            </Link>
            <Link
              className="inline-flex items-center bg-red-400 border-0 py-1 px-3 focus:outline-none hover:bg-red-500 rounded text-white"
              to={"/login"}
            >
              Iniciar sesión
              <svg
                fill="none"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                className="w-4 h-4 ml-1"
                viewBox="0 0 24 24"
              >
                <path d="M5 12h14M12 5l7 7-7 7"></path>
              </svg>
            </Link>
          </div>
        )}
      </div>
    </header>
  );
}
