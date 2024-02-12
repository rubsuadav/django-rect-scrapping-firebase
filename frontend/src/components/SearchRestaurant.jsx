import React, { useState } from "react";
import Swal from "sweetalert2";
import { Link } from "react-router-dom";

export default function SearchRestaurant() {
  const [name, setName] = useState("");
  const [restaurant, setRestaurant] = useState([]);
  const [isOpen, setIsOpen] = useState(false);

  async function getRestaurantByName(e) {
    e.preventDefault();
    const response = await fetch(
      `http://127.0.0.1:8000/api/restaurants/search/?search=${name}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    const data = await response.json();
    switch (response.status) {
      case 200:
        setRestaurant(data);
        setIsOpen(true);
        break;
      case 404:
        setRestaurant({});
        Swal.fire({
          icon: "info",
          title: data.error,
        });
        break;
      default:
        break;
    }
  }

  return (
    <div className="flex items-center justify-center">
      <form
        className="w-64"
        method="get"
        onSubmit={(e) => getRestaurantByName(e)}
      >
        <div className="flex items-center bg-white rounded-full shadow-xl">
          <input
            className="rounded-l-full w-full py-2 px-6 text-gray-700 leading-tight focus:outline-none"
            id="search"
            type="text"
            value={name}
            required
            onChange={(e) => setName(e.target.value)}
            placeholder="Buscar restaurantes..."
          />
          <div className="p-2">
            <button className="bg-blue-500 text-white rounded-full p-2 hover:bg-blue-400 focus:outline-none w-12 h-12 flex items-center justify-center">
              🔍
            </button>
          </div>
        </div>
        {isOpen && (
          <div className="absolute mt-2 w-64 rounded-md shadow-lg bg-black z-50">
            <ul>
              <li onClick={() => setIsOpen(false)}>
                <Link
                  to={`/restaurant/${restaurant.nombre.replace(/ /g, "")}`}
                >
                  {restaurant.nombre}
                </Link>
              </li>
            </ul>
          </div>
        )}
      </form>
    </div>
  );
}
