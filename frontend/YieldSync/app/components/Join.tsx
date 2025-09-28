import React from "react";

const Join = () => {
	return (
		<div className="mt-30 flex items-center justify-center">
			<div className="w-[80%] lg:w-[832px] text-center">
				<h1 className="text-5xl text-[#3a33fe] mb-10 md:mb-5">
					Join Us <br />{" "}
					<span className="text-sm font-light text-blue-500 italic  ">
						Be part of the Team!
					</span>
				</h1>
				<p className="mb-7">
					We’re building a future where DeFi is simple, secure, and social.
					Whether you’re new to crypto or a seasoned investor, YieldSync is here
					to help you sync your investments with the opportunities of tomorrow.{" "}
					<br /> <br />
					If you&apos;re interested,{" "}
					<span className="text-shadow-blue-400 text-shadow-2xs">Join the Team now!</span>
				</p>
				<button className=" text-[#000000] px-7 py-2 rounded-3xl transition-all duration-300 bg-[#00a2ff] shadow-[0_1px_15px_#00a2ff] cursor-pointer">
					Join Us
				</button>
			</div>
		</div>
	);
};

export default Join;
