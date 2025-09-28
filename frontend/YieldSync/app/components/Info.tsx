import React from 'react'

const Info = () => {
  return (
      <div className=" pt-6 mt-20">
           <h1 className='pb-10 text-[35px] font-semibold text-center'>Get In Touch</h1>

<div className="box w-[300px] min-[350px]:w-[90%] bg-black border-white/40 border-2 rounded-2xl m-auto gap-y-5 gap-x-10 grid grid-cols-2 pt-10 min-[574px]:w-[500px] ">
  <div className="phone w-full mb-5 flex flex-col items-center text-center">
    <svg xmlns="http://www.w3.org/2000/svg" width={24} height={24} viewBox="0 0 24 24">
      <path
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233a14 14 0 0 0 6.392 6.384"
      />
    </svg>
    <p className="font-semibold mt-2 mb-2">Phone</p>
    <p className="text-[13px]">+234 701 444 0285</p>
    <p className="text-[13px]">+356 9998 9227</p>
  </div>

  <div className="email w-full mb-5 flex flex-col items-center text-center pr-9">
    <svg xmlns="http://www.w3.org/2000/svg" width={24} height={24} viewBox="0 0 24 24">
      <path
        fill="currentColor"
        d="M4 20q-.825 0-1.412-.587T2 18V6q0-.825.588-1.412T4 4h16q.825 0 1.413.588T22 6v12q0 .825-.587 1.413T20 20zM20 8l-7.475 4.675q-.125.075-.262.113t-.263.037t-.262-.037t-.263-.113L4 8v10h16zm-8 3l8-5H4zM4 8v.25v-1.475v.025V6v.8v-.012V8.25zv10z"
      />
    </svg>
    <p className="font-semibold mt-2 mb-2">Email</p>
    <p className="text-[13px]">emenikesteph@gmail.com</p>
    <p className="text-[13px]">jaminonuegbu@gmail.com</p>
  </div>

  <div className="whatsapp w-full mb-5 flex flex-col items-center text-center">
    <svg xmlns="http://www.w3.org/2000/svg" width={24} height={24} viewBox="0 0 24 24">
      <path
        fill="currentColor"
        d="M19.05 4.91A9.82 9.82 0 0 0 12.04 2c-5.46 0-9.91 4.45-9.91 9.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91c0-2.65-1.03-5.14-2.9-7.01m-7.01 15.24c-1.48 0-2.93-.4-4.2-1.15l-.3-.18l-3.12.82l.83-3.04l-.2-.31a8.26 8.26 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.24-8.24c2.2 0 4.27.86 5.82 2.42a8.18 8.18 0 0 1 2.41 5.83c.02 4.54-3.68 8.23-8.22 8.23m4.52-6.16c-.25-.12-1.47-.72-1.69-.81c-.23-.08-.39-.12-.56.12c-.17.25-.64.81-.78.97c-.14.17-.29.19-.54.06c-.25-.12-1.05-.39-1.99-1.23c-.74-.66-1.23-1.47-1.38-1.72c-.14-.25-.02-.38.11-.51c.11-.11.25-.29.37-.43s.17-.25.25-.41c.08-.17.04-.31-.02-.43s-.56-1.34-.76-1.84c-.2-.48-.41-.42-.56-.43h-.48c-.17 0-.43.06-.66.31c-.22.25-.86.85-.86 2.07s.89 2.4 1.01 2.56c.12.17 1.75 2.67 4.23 3.74c.59.26 1.05.41 1.41.52c.59.19 1.13.16 1.56.1c.48-.07 1.47-.6 1.67-1.18c.21-.58.21-1.07.14-1.18s-.22-.16-.47-.28"
      />
    </svg>
    <p className="font-semibold mt-2 mb-2">Whatsapp</p>
    <p className="text-[13px]">+356 9998 9227</p>
    <p className="text-[13px]">+234 808 841 0949</p>
  </div>

  <div className="location w-full mb-5 flex flex-col items-center text-center pr-9">
    <svg xmlns="http://www.w3.org/2000/svg" width={24} height={24} viewBox="0 0 24 24">
      <path
        fill="currentColor"
        d="M12 2C7.589 2 4 5.589 4 9.995C3.971 16.44 11.696 21.784 12 22c0 0 8.029-5.56 8-12c0-4.411-3.589-8-8-8m0 12c-2.21 0-4-1.79-4-4s1.79-4 4-4s4 1.79 4 4s-1.79 4-4 4"
      />
    </svg>
    <p className="font-semibold mt-2 mb-2">Location</p>
    <p className="text-[13px]">we&apos;re working on it..</p>
  </div>
</div>

            
        </div>
  )
}

export default Info