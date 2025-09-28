import React from 'react'
import NavBar from './NavBar'
import Hero from './Hero'
import './Container.css'


const Container = () => {
  return (
    <div className='container'>
    <NavBar />
    <Hero />
    </div>
  )
}

export default Container