import { summaryInfo } from "@/data/summaryInfo";
import React from "react";
import Image from "next/image";
import { recommendInfo } from "@/data/recommendationInfo";
import RecommendationCard from "../components/RecommendationCard";

const Dashboard = () => {
  return (
    // ✅ Remove flex-1 min-w-0 - let Layout handle it
    <div className="p-3 mb-10">
      <div className="header mt-3 mb-20 sm:mb-10">
        <h1 className="text-3xl">Dashboard</h1>
        <p className="ml-2 text-sm text-[#8498b9]">Overview of your assets and recommendations</p>
      </div>

      <div className="summary mb-20 sm:mb-10">
        <h2 className="text-2xl">Summary</h2>
        <div className="flex flex-col sm:flex-row gap-5 min-[1096px]:gap-12 mt-10 ml-3 sm:ml-10">
          {summaryInfo.map(summary => (
            <div className="bg-[#070550] border-[#7E8BFF] border-2 p-3 rounded-2xl sm:w-[250px] h-[100px] min-[1096px]:w-xl min-[1096px]:h-[120px]" key={summary.id}>
              <h3 className="text-[#8498b9] mb-4">{summary.name}</h3>
              <p className="ml-3 font-semibold text-2xl">{summary.money ? `$${summary.value}` : `${summary.value}`}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="recommendations mb-20 sm:mb-10 flex flex-col  w-full">
        <h2 className="text-2xl">Top Recommendations</h2>
        <div className="mt-7 flex-wrap flex-row flex min-[450px]:flex-col justify-center items-center min-[450px]:items-start md:ml-9 gap-6">
          {recommendInfo.map((rec) => (
           <RecommendationCard key={rec.id} name={rec.name} risk={rec.risk}/>
          ))}
        </div>
      </div>

      <div className="quick-actions">
        <h2 className="text-2xl">Quick Actions</h2>
        <div className="quick-btns mt-4">
          <button className="w-[46%] py-3 lg:w-[400px] rounded-3xl  mr-7 md:mr-7 cursor-pointer p-2 bg-[#070550]">Manage Wallets</button>
          <button className="w-[46%] py-3 lg:w-[400px] cursor-pointer p-2 rounded-3xl bg-[#00a2ff]">Explore Pools</button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
