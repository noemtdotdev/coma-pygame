import pageData from "../constants/page.json";

const Header = () => {

  return (
    <header className="bg-neutral-800 text-white py-4 px-6 flex items-center justify-between mb-4 rounded-b-xl mx-4 relative shadow-xl">
      <div className="flex items-center flex-grow">
        <img
          src="/assets/icon.webp"
          className="w-10 h-10 md:w-12 md:h-12 mr-4 rounded-lg"
          alt="logo"
        />
        <h1 className="text-xl md:text-2xl text-white">{pageData.pageName}</h1>
      </div>
    </header>
  );
};
export default Header;