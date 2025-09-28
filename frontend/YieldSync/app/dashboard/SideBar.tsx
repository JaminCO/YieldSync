import React from "react";
import Image from "next/image";
import { useSideBar } from "./SideBarContext";
import SideNavItem from "./SideNavItem";
import { navItem } from "@/data/navItem";
import { usePathname } from "next/navigation";

const SideBar = () => {
	const pathname = usePathname();
	const { isOpen, closeSideBar } = useSideBar();
	return (
		<>
			{/* Overlay - Mobile only */}
			{isOpen && (
				<div
					className="fixed inset-0 bg-black/20 opacity-80 bg-opacity-50 z-40 lg:hidden"
					onClick={closeSideBar}
				/>
			)}

			{/* Sidebar - Modified for desktop closeable behavior */}
			<div
				className={`fixed inset-y-0 left-0 z-50 bg-[#2A2F40] shadow-[0px_4px_12px] shadow-gray-900 transform transition-all duration-300 ease-in-out lg:relative lg:z-auto lg:flex-shrink-0 ${
					isOpen
						? "w-64 translate-x-0"
						: "w-0 -translate-x-full lg:translate-x-0 lg:w-0"
				}`}
			>
				<div className={`w-64 ${isOpen ? "block" : "hidden lg:hidden"}`}>
					<div className="logo flex items-center justify-between px-2 mt-5">
						<Image
							src={"/YieldSync_Banner_cutout.png"}
							alt="YieldSync Logo"
							width={160}
							height={70}
						/>

						{/* ✅ Remove lg:hidden - allow closing on all screens */}
						<Image
							src={"/close-dashboard.svg"}
							alt="Close Sidebar"
							width={30}
							height={30}
							className="cursor-pointer mt-2"
							onClick={closeSideBar}
						/>
					</div>
					<div className="nav-items mt-10">
						{navItem.map((item) => {
							const isActive = pathname === item.href;

							return (
								<SideNavItem
									key={item.id}
									name={item.name}
									href={item.href}
									image={item.image}
									isActive={isActive}
								/>
							);
						})}
					</div>
				</div>
			</div>
		</>
	);
};

export default SideBar;
