import React from "react";
import { useLocation } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";

const NotFoundPage = () => {
  const location = useLocation();

  return (
    <div className="flex flex-col min-h-screen text-white bg-gray-800">
      <Header />
      <main className="container mx-auto flex-grow flex items-center justify-center px-8 py-12">
        <section className="text-center">
          <div className="flex items-center justify-center mb-8">
            <span className="text-6xl font-bold">4</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="-11.5 -10.23174 23 20.46348"
              className="w-24 h-24 mx-4"
            >
              <title>O</title>
              <circle cx="0" cy="0" r="2.05" fill="#61dafb" />
              <g stroke="#61dafb" strokeWidth="1" fill="none">
                <ellipse rx="11" ry="4.2" />
                <ellipse rx="11" ry="4.2" transform="rotate(60)" />
                <ellipse rx="11" ry="4.2" transform="rotate(120)" />
              </g>
            </svg>
            <span className="text-6xl font-bold">4</span>
          </div>
          <h2 className="text-5xl font-bold mb-4">404 - Page Not Found</h2>
          <p className="text-xl mb-8">
            Sorry, the page you are looking for does not exist.
          </p>
          <button
            onClick={() => {
              window.location.href = "/";
            }}
            className="inline-block px-6 py-3 bg-blue-600 text-white text-2xl rounded-lg hover:bg-blue-700 transition duration-300"
          >
            Return to Home
          </button>
          {location.pathname === "/404" && (
            <div className="mt-8 text-2xl text-yellow-500">
              🤨 Why are you even trying to land here?
            </div>
          )}
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default NotFoundPage;