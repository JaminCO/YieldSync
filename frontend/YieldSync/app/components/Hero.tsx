import React from "react";


const Hero = () => {
	return (
		<div className=" my-auto xl :">
			<div className="flex flex-col lg:flex-row gap-6 mt-25 lg:mt-15 mx-8 items-center justify-center  ">
				<div className=" text-center mt-13 md:mt-32 ">
					<h1 className="text-[35px] sm:text-[48px] md:text-[55px] font-bold xl:leading-20 leading-14 text-center   ">
						Smarter DeFi Investments, Powered by AI.
					</h1>
          <p className="text-base sm:text-xl mt-8 text-center">
            YieldSync analyzes your wallet and recommends the best <br /> pools to maximize returns — explained in plain English.
          </p>
					<button className="bg-[#00D4FF] text-[#000000] mt-8 px-7 py-3 rounded-3xl lg:px-12 lg:text-lg cursor-pointer sm:inline-block">
						Get Early Access
					</button>
				</div>
				
			</div>
		</div>
	);
};

export default Hero;
