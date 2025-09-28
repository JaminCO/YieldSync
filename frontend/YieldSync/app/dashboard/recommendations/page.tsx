import React from 'react'
import RecommendationCard from '@/app/components/RecommendationCard'
import { recommendInfo } from '@/data/recommendationInfo'

const Recommendations = () => {
  return (
    <div className='flex justify-center p-3 '>
      <div className=''>
        <div className="header text-center">
          <h1 className='text-3xl mt-10 mb-3'>AI-Powered Recommendations</h1>
          <p className='text-gray-400 mb-10'>Manage your AI recommendations</p>
        </div>

         
        <div className="mt-7 flex-wrap flex-row flex min-[450px]:flex-col min-[650px]:w-[600px] min-[800px]:w-[700px] justify-center items-center min-[450px]:items-start lg:w-[900px] md:ml-9 gap-6">
          {recommendInfo.map((rec) => (
           <RecommendationCard key={rec.id} name={rec.name} risk={rec.risk}/>
          ))}
        
        </div>
         
      </div>
      </div>
    
  )
}

export default Recommendations