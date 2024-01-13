'use client';
import { useRouter } from "next/navigation";
export default function NavBar() {
    const router = useRouter()
    return(
    <div className=' rounded-lg mx-2 mt-2 text-center min-h-20 grid grid-cols-4 bg-emerald-700'>
    <div className='text-left p-4 underline decoration-double decoration-emerald-900 text-white text-5xl font-bold mb-4'>Spinich</div>
    <button className='p-4 text-xl hover:bg-emerald-400' onClick={() => router.push('/dashboard')}>Dashboard</button>
    <button className="p-4 text-xl hover:bg-emerald-400" onClick={() => router.push('/send')}>Send</button>
    <button className="p-4 text-xl hover:bg-emerald-400" onClick={() => router.push('/template')}>Edit Templates</button>

  </div>)
}