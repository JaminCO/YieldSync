'use client'
import React from "react";
import Image from "next/image";
import Link from "next/link";

interface SideNavItemProps {
	name: string;
	image: string;
	href: string;
	isActive: boolean;
}

const SideNavItem = ({ name, image, href, isActive }: SideNavItemProps) => {
	return (
		<Link
			href={href}
			className={`flex w-[90%]  px-3 gap-3 items-center cursor-pointer hover:bg-[#00D4FF] py-4 duration-500 transition-colors  ${
				isActive && " bg-[#001437]"
			}`}
		>
			<Image src={image} alt="dashboard icon" width={26} height={30} />
			<p>{name}</p>
		</Link>
	);
};

export default SideNavItem;
