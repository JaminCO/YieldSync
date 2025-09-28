import React from 'react'
import Image from 'next/image'
interface SupportedChainProps {
    name: string
  }
const SupportedChain = ({name}: SupportedChainProps) => {
  
  return (
    <div className='flex gap-3 py-4 px-2  w-[138px]  sm:px-5 bg-blue-950 border-1 border-[#464a6b] rounded-xl sm:w-[170px]'>
      <Image src={'/recommendation-img.png'} alt='placeholder-img' width={50} height={100} className='w-[30px]' />
      <p>{name}</p>
    </div>
  )
}

export default SupportedChain