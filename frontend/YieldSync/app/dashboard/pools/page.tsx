import React from 'react'
import Table from './Table'

const Pools = () => {
  return (
    <div className='flex flex-col justify-center items-center p-3 mt-10'>
      <div className="header text-center">
 <h1 className='text-3xl mb-2'>AI-Powered Yield Opportunities</h1>
      <p className='text-gray-400 mb-5'>Explore AI-generated recommendations for optimal yield strategies across multiple chains</p>

      </div>

      <div className="search mb-4 ">
        <input className='bg-blue-950 p-3 rounded-3xl w-[290px] min-[500px]:w-[450px] min-[730px]:w-[600px]' type="search" name="search" id="search" placeholder='Search'/>
      </div>

      <div className="filter mb-17 flex justify-start w-full max-w-[700px] min-[500px]:pl-10">
        <button className='py-3 px-6 bg-[#00a2ff] cursor-pointer rounded-3xl'>Filter:coming soon..</button>
      </div>

     
      <Table />
    </div>
  )
}

export default Pools