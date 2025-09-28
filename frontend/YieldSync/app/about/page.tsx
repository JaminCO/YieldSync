import React from "react";
import AboutCards from "../components/AboutCards";
import NavBar from "../components/NavBar";
import { aboutInfo } from "../../data/aboutInfo";
import AboutImg from "../../public/AboutImgs.jpg";
import ValueCard from "../components/ValueCard";
import { valueInfo } from "@/data/valueInfo";
import Join from "../components/Join";
import FounderCard from "../components/FounderCard";
import { founderInfo } from "@/data/founderInfo";
import Info from "../components/Info";

const About = () => {
	return (
		<div
			className="h-fit  pb-30"
			style={{
				backgroundImage: `url(${AboutImg.src})`,
				backgroundPosition: "center",
				backgroundSize: "cover",
			}}
		>
			<NavBar />

			<h1 className="about-head text-center font-semibold text-4xl sm:text-5xl mt-15 mb-20 ">
				About Us <br />
				<span className="text-sm font-light text-blue-500 italic -mt-4 ">
					Learn about YieldSync team
				</span>
			</h1>

			<div className="about-cards flex-col sm:flex-row gap-7 flex items-center justify-center flex-wrap mb-30">
				{aboutInfo.map((info) => (
					<AboutCards key={info.id} header={info.header} answer={info.answer} />
				))}
			</div>

			<div className="values">
				<h1 className="text-center mb-15 text-5xl">Our <span className="text-[#3a33fe]">Values</span> <br />
        <span  className="text-sm font-light text-blue-500 italic -mt-4 ">What we stand for</span>
        </h1>
				<div className="value-cards flex flex-col min-[420px]:flex-row gap-7 items-center justify-center flex-wrap xl:gap-20">
					{
            valueInfo.map(info=>(
              <ValueCard key={info.id} value={info.value} body ={info.body} number={info.id}/>
            ))
          }
				</div>
			</div>
			<div className="founders mt-45">
				<h1 className="text-center mb-19 text-5xl">Meet The Founders <br /> <span  className="text-sm font-light text-blue-500 italic -mt-4 ">The faces behind the product</span></h1>
				<div className="founder-cards flex flex-col items-center justify-center gap-7 md:gap-5 sm:flex-row lg:gap-23">
          {
						founderInfo.map(info=>(
							<FounderCard key={info.id} name={info.name} image={info.image} position={info.position} bio={info.bio} linkedin={info.linkedinLink} github={info.githubLink} />
						))
					}

				</div>

			</div>
			<Join />
      <Info />
		</div>
	);
};

export default About;
