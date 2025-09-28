import ConnectedWallets from '@/app/components/ConnectedWallets'
import SupportedChain from '@/app/components/SupportedChain'
import { supportedChainInfo } from '@/data/supportedChainInfo'
import React from 'react'
import Link from 'next/link'

const Wallet = () => {
  return (
    <div className='p-3 flex justify-center items-center flex-col text-center mt-10 mb-5'>
      <div className="main">
        <div className="header mb-10">
        <h1 className='text-4xl mb-3'>Connect Wallet</h1>
        <p className='text-gray-400'>Manage your DeFi assets across multiple chains securely and efficiently.</p>
        </div>

        <div className="supported mt-13 min-[804]:w-[780px]">
          <h3 className='text-left text-xl mb-4'>Supported Chains</h3>
          <div className="supported-chains flex flex-wrap justify-center gap-4 ">
          {
            supportedChainInfo.map(info=>(
              <SupportedChain key={info.id} name={info.name} />
            ))
          }
         
        </div>
        </div>

      

        <div className="connected-wallets mt-10">
          <h3 className='text-left text-xl mb-4'>Connected Wallets</h3>
          <div>
            <ConnectedWallets />
            <ConnectedWallets />
            <ConnectedWallets />
          </div>
          

        </div>

        <Link href={'/sign-up/connect-wallet'}>
           <button className='bg-[#00a2ff] border-1 mt-9 border-[#7E8BFF] cursor-pointer w-[300px] py-3 rounded-4xl'>Connect Wallet</button>
        </Link>

        

      </div>
    </div>
  )
}

export default Wallet