import React, { useState } from "react";
import { Link } from "react-router-dom";
import { BeatLoader } from "react-spinners";

export default function Chat() {
  const userId = localStorage.getItem("userId");
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const addMessage = (newMessage) => {
    setMessages((prevMessages) => [...prevMessages, newMessage]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const userMessage = {
      prompt: message,
      fromUser: true,
    };
    addMessage(userMessage);

    const response = await fetch("http://127.0.0.1:8000/api/chat/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
        prompt: message,
      }),
    });
    const responseData = await response.json();

    const botMessage = {
      prompt: responseData.prompt,
      response: responseData.response.response,
      fromUser: false,
    };
    addMessage(botMessage);

    setMessage("");
    setLoading(false);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <div className="flex flex-col flex-1 overflow-y-auto p-8 m-4 bg-white rounded shadow-md">
        <h2 className="text-2xl font-bold text-center mb-4">Chat con el bot</h2>
        <div className="flex flex-col flex-1 mb-4 space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex flex-col items-start ${
                message.fromUser ? "items-end" : ""
              }`}
            >
              {message.fromUser && (
                <p className="text-sm bg-blue-200 rounded-lg p-2 m-2 text-right">
                  <strong>Usuario:</strong> {message.prompt}
                </p>
              )}
              {!message.fromUser && message.response && (
                <p className="text-sm bg-green-200 rounded-lg p-2 m-2">
                  <strong>IA:</strong> {message.response}
                </p>
              )}
            </div>
          ))}
          {loading && (
            <div className="flex justify-center">
              <BeatLoader color={"#123abc"} loading={loading} size={15} />
            </div>
          )}
        </div>
        <form onSubmit={handleSubmit} className="mt-auto">
          <div className="mb-4">
            <input
              type="text"
              className="w-full px-3 py-2 leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline"
              placeholder="Escribe tu mensaje"
              name="prompt"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />
          </div>

          <div className="flex space-x-4">
            <button
              type="submit"
              className="w-auto px-2 py-2 font-bold text-white bg-blue-500 rounded hover:bg-blue-700 focus:outline-none focus:shadow-outline"
            >
              Enviar
            </button>
            <Link
              className="w-auto px-1 py-3 font-bold text-white bg-red-500 rounded hover:bg-red-700 focus:outline-none focus:shadow-outline"
              to="/"
            >
              Cancelar
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
