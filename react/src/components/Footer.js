import React, { useMemo } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCopyright } from "@fortawesome/free-regular-svg-icons";
import pageData from "../constants/page.json";
import { useLocation } from "react-router-dom";

const Footer = () => {
  const currentYear = new Date().getFullYear();
  const location = useLocation();

  const textAboveLinks = useMemo(() => pageData.footer.textAboveLinks, []);
  const links = useMemo(() => pageData.footer.links, []);
  const pageName = useMemo(() => pageData.pageName, []);
  const copyrightUrl = useMemo(() => pageData.footer.copyrightUrl, []);
  const copyright = useMemo(() => pageData.footer.copyright, []);

  return (
    <footer className="rounded-lg m-4 bg-neutral-800 text-gray-400">
      <div className="w-full max-w-screen-xl mx-auto p-4 md:py-8">
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center">
          <a
            href={location.pathname}
            className="flex items-center mb-4 sm:mb-0 space-x-3 rtl:space-x-reverse"
          >
            <img src="/assets/icon.webp" className="h-8" alt="logo" />
            <span className="text-2xl">{pageName}</span>
          </a>
          <div className="w-full sm:w-auto sm:ml-auto text-right">
            {textAboveLinks.map((text, index) => (
              <p key={index} className="mb-4 mr-4 md:mr-6">
                {text}
              </p>
            ))}
            <ul className="flex flex-wrap items-center justify-end text-sm">
              {links.map((link, index) => (
                <li key={index} className="mr-4 md:mr-6">
                  <a href={link.href}>
                    {link.icon ? <i className={link.icon}></i> : link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>
        <hr className="my-6 border-gray-600 sm:mx-auto lg:my-8" />
        <div className="text-sm sm:text-center">
          <span className="inline-flex items-center">
            <FontAwesomeIcon icon={faCopyright} />
            <span className="ml-1">
              {currentYear}&nbsp;
              <a href={copyrightUrl}>{copyright}</a>
              &nbsp;|&nbsp;All rights reserved.
            </span>
          </span>
        </div>
      </div>
    </footer>
  );
};

export default Footer;