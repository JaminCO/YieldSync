"use client";
//  createContext → makes the “shared box”.
// useContext → lets components read from the box.
// useState → keeps track of whether sidebar is open.
// useEffect → run extra logic when the screen resizes.
import { createContext, useContext, useState, useEffect } from "react";

//the functions and variables we'll need for the context
type SideBarContextType = {
	isOpen: boolean; // is sidebar visible?
	toggleSideBar: () => void; // flip open/close
	closeSideBar: () => void; // force close
	openSideBar: () => void; // force open
};

//creating the context
const SideBarContext = createContext<SideBarContextType | undefined>(undefined);

//The provider
export function SideBarProvider({ children }: { children: React.ReactNode }) {
	const [isOpen, setIsOpen] = useState(false);

	//auto-open on big screens
	useEffect(() => {
		function handleResize() {
			if (window.innerWidth >= 1191) {
				setIsOpen(true);
			} else {
				setIsOpen(false);
			}
		}
		handleResize();
		window.addEventListener("resize", handleResize);
		return () => {
			window.removeEventListener("resize", handleResize);
		};
	}, []);

	//functions for control, or helper functions, we pass them into the context so that any component can call them

	const toggleSideBar = () => setIsOpen((prev) => !prev);
	const closeSideBar = () => {setIsOpen(false)  
    console.log('closed')};
	const openSideBar = () => setIsOpen(true);

	//toggleSidebar() → flip state (true → false, false → true).
	// closeSidebar() → force close.
	// openSidebar() → force open.

	return (
		<SideBarContext.Provider
			value={{ isOpen, toggleSideBar, closeSideBar, openSideBar }}
		>
			{children}
		</SideBarContext.Provider>
		// We put isOpen + our functions into the “box”, and wrap children with it.
		// Now, anything inside SidebarProvider can use useSidebar() to read or change the sidebar
		//
	);
}

//The Hook
export function useSideBar() {
	const context = useContext(SideBarContext);
	if (!context) {
		throw new Error("useSideBar must be used inside SidebarProvider");
	}
	return context;

	//   This is just a shortcut.
	// Instead of writing useContext(SidebarContext)    everywhere, we can just write useSidebar().
}
