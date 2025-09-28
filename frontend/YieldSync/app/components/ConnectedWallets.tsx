import React from 'react'
import Image from 'next/image'

const ConnectedWallets = () => {
  return (
    <div className='flex justify-between items-center bg-blue-950 border-1 border-[#464a6b] p-2'>
      <div className='flex items-center gap-4'>
        <Image src={'/wallet-icon.svg'} alt='wallet-icon' width={34} height={24} />

        <div className="wallet-info">
          <p className="wallet-address font-semibold">
            0x1a2b...c3d4
          </p>
          <p className="wallet-chain text-gray-400">
            Etheruem
          </p>
        </div>

       
      </div>
       <Image src={'/delete-icon.svg'} alt='delete-icon' width={24} height={24} />
    </div>
  )
}

export default ConnectedWallets