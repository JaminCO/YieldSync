import React from 'react'

interface ValueCardProps {
  number: number,
  value: string,
  body: string
}

const ValueCard = ({number, value, body}: ValueCardProps) => {
  return (
    <div className='border-2 border-blue-300/30 bg-white/5 rounded-2xl px-4 py-2 w-[200px] h-[200px] hover:-translate-y-3 duration-1000 hover:shadow-[0px_4px_12px_blue]' >
      <h1 className='font-semibold text-4xl mb-3 -ml-2'>{number}</h1>
      <h4 className='font-semibold text-lg mb-3'>{value}</h4>
      <p className=''>{body}</p>
    </div>
  )
}

export default ValueCard