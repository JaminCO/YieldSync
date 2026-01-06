'use client'
import { recommendInfo } from '@/data/recommendationInfo'
import { useParams } from 'next/navigation'
import React from 'react'

interface DetailsProps {
  params: {id:number}
}

const RecommendationDetails = ({params}:DetailsProps) => {
 
  // const {id} = useParams()
  // const info = recommendInfo.find(item=> item.id === params.id)
  // console.log(info)

  // if (!info) {
  //   return(<div className='flex justify-center items-center h-screen'>Page not found</div>)
  // } else
  return (
    <div className='p-3  lg:w-[80%] flex flex-col items-center justify-center'>
      <div>
        <h1 className='text-3xl mb-3'>Recommendation Details</h1>
        <p className='text-gray-400 mb-14'>Explore details of this AI-powered recommendation to understand its potential and associated risks</p>

        <div className="grid  sm:grid-cols-2 gap-x-7 sm:gap-y-5  gap-y-9 ">
          <div className="explain bg-[#070550] border-[#7E8BFF] border-3 p-3 rounded-2xl">
            <h3 className='text-xl font-medium mb-4'>AI Explanation</h3>
            <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Veritatis veniam excepturi cumque voluptatibus consequuntur dignissimos maiores recusandae repellendus velit! Necessitatibus, sequi. Earum ducimus necessitatibus eveniet. Modi alias iusto veritatis, commodi ad qui dignissimos quo iure at neque similique ducimus maiores.</p>
          </div>

          <div className="risk  bg-[#070550] border-[#7E8BFF] border-3 p-3 rounded-2xl">
            <div className="overall flex justify-between items-center mb-2">
              <p className='text-lg'>Overall Risk</p>
              <h3 className='text-xl font-semibold' >75%</h3>
            </div>
            <hr className='mb-4' />
            <div className="liquidity flex justify-between items-center mb-3">
              <p>Liquidity risk</p>
              <p className='text-red-400'>Low</p>
            </div>
            <div className="smart flex justify-between items-center mb-3">
              <p>Smart Contract Risk</p>
              <p className='text-yellow-400'>Moderate</p>
            </div>
            <div className="market flex justify-between items-center mb-3">
              <p>Market Risk</p>
              <p className='text-green-400'>High</p>
            </div>
            <div className="operations flex justify-between items-center mb-3">
              <p>Operational Risk</p>
              <p className='text-red-400'>Low</p>
            </div>
          </div>

          <div className="details  bg-[#070550] border-[#7E8BFF] border-3 p-3 rounded-2xl">
            <div className="flex justify-between items-center border-b-2 py-3">
              <p className='font-semibold'>Pool Name</p>
              <p>Stablecoin</p>
              
            </div>
            
            <div className="chain flex justify-between items-center border-b-2 py-3">
              <p className='font-semibold'>Chain</p>
              <p>Ethereum</p>
            </div>
            <div className='flex justify-between items-center border-b-2 py-3'>
              <p className='font-semibold'>APY</p>
              <p>12.5%</p>
            </div>
            <div className='flex justify-between items-center border-b-2 py-3'>
              <p className='font-semibold'>TVL</p>
              <p> $50M</p>
            </div>
            <div className='flex justify-between items-center py-3'>
              <p className='font-semibold'>Underlying Assets</p>
              <p> USDC,USDT,DAI</p>
            </div>
          </div>
          <div className="btn flex justify-center items-center">
            <button className='bg-[#00a2ff] text-white px-4 py-2 w-[300px] sm:self-start sm:mt-7 rounded-3xl cursor-pointer'>Invest Now</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default RecommendationDetails