'use client'
import React from 'react'
import Link from 'next/link'
import Image from 'next/image'

interface FounderCardProps {
  name: string,
  image: string,
  position: string,
  bio: string,
  linkedin: string,
  github: string
}

const FounderCard = ({name, image, position, bio, linkedin, github}: FounderCardProps) => {
  return (
    <div>
      <div className=" border-2 border-white/50 bg-white/10 w-[270px] rounded-2xl flex flex-col items-center text-center px-4 py-4 sm:w-[300px] md:w-[365px] lg:w-[400px] hover:-translate-y-6 duration-1000">
        <Image className='rounded-[100px] w-[150px] h-[150px] object-cover mb-2' src={image} width={100} height={100} alt='' />
        <p className="name font-semibold mb-1 text-lg">{name}</p>
        <p className="title font-semibold text-sm mb-3">{position}</p>
        <p className="bio">{bio}</p>
        <div className="links flex gap-4 mt-5 items-center">
          <Link href={github}>
          <Image width={25} height={20} src='/github.svg' alt='github icon' />
          </Link>

            <Link href={linkedin}>
          <Image width={25} height={20} src={'/linkedin.svg'} alt='LinkedIn icon' />
          </Link>
        </div>
      </div>
    </div>
  )
}

export default FounderCard