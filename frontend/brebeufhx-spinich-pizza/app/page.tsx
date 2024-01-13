'use client'
import React, {useEffect, useState} from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {faPizzaSlice, faCheese } from '@fortawesome/free-solid-svg-icons'
import { useRouter } from 'next/navigation'

export default function Home() {
  const [cheeseCount, setCheeseCount] = useState(0)
  const router = useRouter()
  useEffect(() => {
    router.push('/login')
  }, [])
  return (""
  )
}
