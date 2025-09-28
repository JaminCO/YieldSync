import React from 'react'
import Image from 'next/image'

interface RecommendationCardProps{
  name: string,
  risk:string
}
const RecommendationCard = ({name, risk}: RecommendationCardProps) => {
  
  return (
     <div  className="bg-[#070550] rounded-2xl flex-col w-[300px]  flex min-[450px]:py-2 min-[450px]:flex-row min-[450px]:max-h-[130px] items-center justify-between min-[450px]:w-[100%] min-[450px]:px-3   ">
                  <div className="flex flex-col min-[450px]:flex-row ">
                    <Image
                      src="/recommendation-img.png"
                      alt="recommended pool image"
                      width={400}
                      height={50}
                      className=" min-[450px]:w-[100px] min-[450px]:h-[70px] w-[300px]  min-[450px]:my-auto rounded-2xl"
                    />
                    <div className="p-4 flex flex-col justify-center leading-4.5">
                      <span className="text-[10px] font-semibold text-[#5fc0f8] uppercase ">Recommended</span>
                      <h3 className="mt-2 font-semibold text-white leading-4.5">{name}</h3>
                      <p className="text-sm text-[#8498b9] leading-4.5">{risk}</p>
                    </div>
                  </div>
                  <div className="p-4 sm:p-0 sm:ml-auto mr-3.5 flex sm:items-center j sm:justify-end">
                    <button className="bg-[#00a2ff] px-6 py-2 rounded-3xl text-white font-medium  hover:bg-[#0090e6] cursor-pointer transition">
                      Explore
                    </button>
                  </div>
                </div>
  )
}

export default RecommendationCard