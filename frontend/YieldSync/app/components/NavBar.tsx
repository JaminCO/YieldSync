
"use client";
import React, { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import logo from "../../public/YieldSync-logo.svg";
import menu from "../../public/menuBar.svg";
import close from "../../public/close.svg";

const NavBar = () => {
  const [toggleMenu, setToggleMenu] = useState(false);

  const links = [
    { name: "Home", href: "/" },
    { name: "About Us", href: "/about" },
    { name: "FAQs", href: "/faqs" },
  ];

  const mobileLinks = [
    { name: "Home", href: "/" },
    { name: "About Us", href: "/about" },
    { name: "FAQs", href: "/faqs" },
    { name: "Sign Up", href: "/sign-up", isButton: true },
  ];

  return (
    <div className="flex justify-between items-center py-4 px-4 md:px-10 relative">
      {/* Logo */}
      <Link href={"/"}>
        <Image className="sm:w-[110px]" width={90} src={logo} alt="Yieldsync logo" />
      </Link>

      {/* Desktop Navigation */}
      <div className="hidden sm:flex bg-white/5 backdrop-blur-lg shadow-lg border border-white/20 rounded-4xl py-3 px-8 gap-12 md:gap-24 lg:gap-40 text-lg justify-center">
        {links.map((link, idx) => (
          <Link
            key={idx}
            href={link.href}
            className="relative group rounded-4xl transition-all duration-300 hover:-translate-y-1"
          >
            {link.name}
            <div className="absolute bottom-0 left-1/2 h-0.5 w-0 bg-blue-400 rounded transition-all duration-300 group-hover:w-3/5 group-hover:-translate-x-1/2"></div>
          </Link>
        ))}
      </div>

      {/* Desktop Sign Up Button */}
      <Link href={"/sign-up"}>
        <button className="hidden sm:inline-block bg-[#00D4FF] text-black px-7 py-3 rounded-3xl lg:px-12 lg:text-base cursor-pointer transition-all duration-300 hover:bg-[#00a2ff] hover:shadow-lg">
          Sign Up
        </button>
      </Link>

      {/* Mobile Menu Button */}
      <Image
        className={`sm:hidden cursor-pointer ${toggleMenu && "hidden"}`}
        width={40}
        onClick={() => setToggleMenu(true)}
        src={menu}
        alt="menu"
      />

      {/* Mobile Overlay */}
      <div
        onClick={() => setToggleMenu(false)}
        className={`fixed inset-0 bg-black/30 backdrop-blur-sm z-40 transition-opacity duration-900 ${
          toggleMenu ? "opacity-100 visible" : "opacity-0 invisible"
        }`}
      ></div>

      {/* Mobile Drawer */}
      <div
        className={`fixed top-0 right-0 h-[70vh] w-[90%] bg-white/50 dark:bg-zinc-900/50 backdrop-blur-md shadow-lg rounded-b-3xl z-50 transform transition-transform duration-900 ${
          toggleMenu ? "translate-y-0" : "-translate-y-full"
        }`}
      >
        {/* Close button */}
        <Image
          onClick={() => setToggleMenu(false)}
          src={close}
          alt="close"
          width={30}
          className="absolute top-4 right-4 cursor-pointer"
        />

        {/* Mobile Links */}
        <div className="flex flex-col mt-16 divide-y divide-white/20">
          {mobileLinks.map((link, idx) =>
            link.isButton ? (
              <Link key={idx} href={link.href} onClick={() => setToggleMenu(false)}>
                <button className="w-[90%] text-center bg-[#00D4FF] text-black px-7 py-3 m-4 rounded-3xl transition-all duration-200 hover:bg-[#00a2ff] hover:shadow-lg">
                  {link.name}
                </button>
              </Link>
            ) : (
              <Link
                key={idx}
                href={link.href}
                onClick={() => setToggleMenu(false)}
                className="block px-6 py-4 hover:bg-blue-400/30 dark:hover:bg-blue-500/20 transition-colors duration-200 rounded-md text-center"
              >
                {link.name}
              </Link>
            )
          )}
        </div>
      </div>
    </div>
  );
};

export default NavBar;


