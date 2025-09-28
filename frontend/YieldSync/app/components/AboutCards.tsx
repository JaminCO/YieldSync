import React from "react";


interface AboutCardsProps {
  header: string,
  answer: string
}

const AboutCards = ({header, answer}: AboutCardsProps) => {
	return (
		<div className="about-card w-[270px] text-center bg-[#070550] border-[#7E8BFF] border-3 rounded-2xl p-4 shadow-[0px_4px_12px_black] sm:w-[340px] max-h-[400px] sm:h-[274px] md:w-[400px] hover:-translate-y-3 duration-1000 hover:shadow-[0px_4px_12px_white]">
			<h3 className="mb-7 font-semibold text-xl text-[#CAC9EE] ">{header}</h3>
			<p>
			{answer}
			</p>
		</div>
	);
};

export default AboutCards;
