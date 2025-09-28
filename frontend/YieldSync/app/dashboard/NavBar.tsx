import React from "react";
import Image from "next/image";
import { useSideBar } from "./SideBarContext";

const NavBar = () => {
	const { toggleSideBar,isOpen } = useSideBar();
	
	if(!isOpen)
	return (
		<nav className=" shadow-sm   px-4 pt-3">
			<div className="flex items-center justify-between">
				{/* Menu button - works on all screen sizes */}
				<button
					onClick={toggleSideBar}
					className="p-2 rounded-md hover:shadow-[0px_4px_12px] shadow-blue-500 transition-colors"
				>
					<Image
						src={"/menuBar.svg"}
						alt="Toggle menu"
						width={24}
						height={24}
					/>
				</button>
				
				{/* Other navbar content */}
				<div className="flex items-center space-x-4">
					{/* Add your navbar items here */}
				</div>
			</div>
		</nav>
	);
};

export default NavBar;