import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

// local imports
import { useAuthContext } from "../../context/authContext";

export default function Login() {
  const { login } = useAuthContext();
  let navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState({});

  const { email, password } = form;

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });

    setErrors({});
  }

  async function handleSubmit(e) {
    e.preventDefault();

    const response = await fetch("http://127.0.0.1:8000/api/auth/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form),
    });
    const data = await response.json();

    switch (response.status) {
      case 200:
        login(data.access_token, data.refresh_token);
        localStorage.setItem("userId", data.userId);
        navigate("/");
        break;
      case 400:
        setErrors(data);
        break;
      case 500:
        setErrors(data.error);
        break;
      default:
        break;
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-8 m-4 bg-white rounded shadow-md">
        <h2 className="text-2xl font-bold text-center mb-4">
          Inicio de sesion
        </h2>
        <form onSubmit={(e) => handleSubmit(e)}>
          <div className="mb-4">
            <label
              htmlFor="Email de usuario"
              className="block mb-2 text-sm font-bold text-gray-700"
            >
              Email
            </label>
            <input
              type="email"
              className="w-full px-3 py-2 leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline"
              placeholder="Escribe tu nombre de usuario"
              name="email"
              value={email}
              onChange={(e) => handleChange(e)}
            />
            {errors.email && (
              <p className="text-red-500 text-xs italic">{errors.email}</p>
            )}
          </div>
          <div className="mb-4">
            <label
              htmlFor="Contraseña"
              className="block mb-2 text-sm font-bold text-gray-700"
            >
              Contraseña
            </label>
            <input
              type="password"
              className="w-full px-3 py-2 leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline"
              placeholder="Escribe tu contraseña"
              name="password"
              value={password}
              onChange={(e) => handleChange(e)}
            />
            {errors.password && (
              <p className="text-red-500 text-xs italic">{errors.password}</p>
            )}
          </div>
          <div className="flex space-x-4">
            <button
              type="submit"
              className="w-auto px-2 py-2 font-bold text-white bg-blue-500 rounded hover:bg-blue-700 focus:outline-none focus:shadow-outline"
            >
              Iniciar sesion
            </button>
            <Link
              className="w-auto px-1 py-3 font-bold text-white bg-red-500 rounded hover:bg-red-700 focus:outline-none focus:shadow-outline"
              to="/"
            >
              Cancelar
            </Link>
            <Link
              className="w-auto px-4 py-2 font-bold text-white bg-green-500 rounded hover:bg-green-700 focus:outline-none focus:shadow-outline text-center"
              to="/register"
            >
              No tienes cuenta? Registrate
            </Link>
          </div>
          <br />
          {errors.message && (
            <p className="text-red-500 text-xs italic">{errors.message}</p>
          )}
        </form>
      </div>
    </div>
  );
}
