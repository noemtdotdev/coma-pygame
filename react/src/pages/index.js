import React from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";

const icons = {
  powerPoint: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Microsoft_Office_PowerPoint_%282019%E2%80%93present%29.svg/2203px-Microsoft_Office_PowerPoint_%282019%E2%80%93present%29.svg.png",
  zip: "/assets/zip.webp",
  github: "https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/github-white-icon.png",
  itch: "https://static-00.iconduck.com/assets.00/itch-io-icon-2048x2048-i6hzclad.png"
}

const Index = () => {
  return (
    <div className="flex flex-col min-h-screen text-white">
      <Header />
      <main className="flex-grow mx-5">
        <div className="flex justify-center my-6">
          <h1 className="text-4xl font-bold">Computermathematik Klausur</h1>
        </div>
        <div className="flex justify-center my-6">
          <img src="/assets/showcase.webp" alt="Showcase" className="w-full lg:w-1/2 "/>
        </div>
        <p className="italic text-center">zu sehen ist Level 8 mit dem Thema "Kunst"</p>
        <div className="flex justify-center my-6">
          <p className="text-xl">Ein Projekt für die Computermathematik. Ein Spiel, welches in Python mit Pygame entwickelt wurde.</p>
        </div>
        <div className="flex flex-col md:flex-row justify-center space-y-4 md:space-y-0 md:space-x-8 my-6">
          <a
            href="/assets/powerpoint.docx"
            download
            className="powerpoint text-white py-2 px-4 rounded flex items-center space-x-2 transition duration-100 transform hover:scale-105 text-sm md:text-base"
          >
            <img src={icons.powerPoint} alt="PowerPoint Icon" className="w-6 h-6" />
            <span>PowerPoint Präsentation</span>
          </a>
          <a
            href="/assets/source.zip"
            download
            className="zip text-white py-2 px-4 rounded flex items-center space-x-2 transition duration-100 transform hover:scale-105 text-sm md:text-base"
          >
            <img src={icons.zip} alt="Source Code Icon" className="w-6 h-6" />
            <span>Source Code</span>
          </a>
          <a
            href="https://github.com/noemtdotdev/coma-pygame"
            target="_blank"
            rel="noopener noreferrer"
            className="github text-white py-2 px-4 rounded flex items-center space-x-2 transition duration-100 transform hover:scale-105 text-sm md:text-base"
          >
            <img src={icons.github} alt="GitHub Icon" className="w-6 h-6" />
            <span>GitHub</span>
          </a>
        </div>
        <div className="flex justify-center my-12">
          <div className="w-full lg:w-1/2">
            <h2 className="text-3xl font-bold text-center mb-6">Credits</h2>
            <div className="p-6 flex flex-col md:flex-row justify-around">
              <div className="text-center m-4 p-4 bg-neutral-800 rounded-lg shadow-lg w-full md:w-1/3">
                <h3 className="text-2xl font-semibold mb-4 text-white">Entwicklung</h3>
                <p className="text-white">Dennis</p>
              </div>
              <div className="text-center m-4 p-4 bg-neutral-800 rounded-lg shadow-lg w-full md:w-1/3">
                <h3 className="text-2xl font-semibold mb-4 text-white">Level Design</h3>
                <p className="text-white">Shani</p>
              </div>
              <div className="text-center m-4 p-4 bg-neutral-800 rounded-lg shadow-lg w-full md:w-1/3">
                <h3 className="text-2xl font-semibold mb-4 text-white">Assets <img src={icons.itch} alt="itch.io Icon" className="inline w-6 h-6 mr-2" /></h3>
                <p className="text-white">
                  Einige Assets von <a href="https://itch.io/game-assets" target="_blank" rel="noopener noreferrer" className="text-white underline hover:text-white hover:no-underline">itch.io
                  </a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Index;