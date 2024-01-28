import React from "react";
import { Link, useNavigate } from "react-router-dom";

// local imports
import { useAuthContext } from "../context/authContext";
import DropDown from "./DropDown";

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
        <nav className="md:mr-auto md:ml-4 md:py-1 md:pl-4 md:border-l md:border-gray-400 flex flex-wrap items-center text-base justify-center">
          <DropDown
            buttonLabel="DESPLEGABLE 1"
            css1="group inline-block text-left relative mr-12"
            css2="inline-flex justify-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white font-medium hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 text-green-600 text-xl"
          >
            <Link
              to={"/"}
              className="block px-4 py-2 text-lg text-white hover:bg-yellow-300 hover:text-gray-900 bg-yellow-700"
              role="menuitem"
            >
              ITEM 1
            </Link>
            <Link
              to={"/"}
              className="block px-4 py-2 text-lg border-t-8 text-white hover:bg-fuchsia-300 hover:text-gray-900 bg-fuchsia-700"
              role="menuitem"
            >
              ITEM 2
            </Link>
          </DropDown>
          <DropDown
            css1="group inline-block text-left relative mr-8"
            css2="inline-flex justify-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white font-medium hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 text-indigo-500 text-xl"
            buttonLabel="DESPLEGABLE 2"
          >
            <Link
              to={"/"}
              className="block px-4 py-2 text-lg text-white hover:bg-blue-300 hover:text-gray-900 bg-blue-700"
              role="menuitem"
            >
              ITEM 1
            </Link>
            <Link
              to={"/"}
              className="block px-4 py-2 text-lg text-white hover:bg-red-300 hover:text-gray-900 border-t-8 bg-red-700"
              role="menuitem"
            >
              ITEM 2
            </Link>
            <Link
              to={"/"}
              className="block px-4 py-2 text-lg text-white hover:bg-green-300 hover:text-gray-900 border-t-8 bg-green-700"
              role="menuitem"
            >
              ITEM 3
            </Link>
            <Link
              to={"/"}
              className="block px-4 py-2 text-lg text-white hover:bg-yellow-300 hover:text-gray-900 border-t-8 bg-yellow-700"
              role="menuitem"
            >
              ITEM 4
            </Link>
            <Link
              to={"/"}
              className="block px-4 py-2 text-lg text-white hover:bg-pink-300 hover:text-gray-900 border-t-8 bg-pink-500"
              role="menuitem"
            >
              ITEM 5
            </Link>
          </DropDown>
        </nav>
        {isAuthenticated && (
          <>
            <Link
              className="inline-flex items-center bg-yellow-600 border-0 py-1 px-3 focus:outline-none hover:bg-yellow-500 rounded mt-4 md:mt-0 text-white text-xl mr-16"
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
              className="inline-flex items-center bg-green-600 border-0 py-1 px-3 focus:outline-none hover:bg-green-400 rounded text-base mt-4 md:mt-0 text-white mr-8"
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
          </>
        )}
        {!isAuthenticated && (
          <>
            <Link
              className="inline-flex items-center bg-blue-400 border-0 py-1 px-3 focus:outline-none hover:bg-blue-500 rounded text-base mt-4 md:mt-0 text-white mr-8"
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
              className="inline-flex items-center bg-red-400 border-0 py-1 px-3 focus:outline-none hover:bg-red-500 rounded text-base mt-4 md:mt-0 text-white mr-8"
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
          </>
        )}
      </div>
    </header>
  );
}
