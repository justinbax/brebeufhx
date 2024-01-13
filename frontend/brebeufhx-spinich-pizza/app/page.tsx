'use client'
import React, {useState} from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {faPizzaSlice, faCheese } from '@fortawesome/free-solid-svg-icons'

export default function Home() {
  const [cheeseCount, setCheeseCount] = useState(0)
  return (
    <main>
      <h1 className="text-3xl">Hello World</h1>
      <button className='rounded-full bg-amber-300 p-2 m-2' onClick={() => setCheeseCount(cheeseCount + 1)}> <FontAwesomeIcon icon={faPizzaSlice}></FontAwesomeIcon> Pizza Counter: {cheeseCount}</button>
    </main>
  )
}
