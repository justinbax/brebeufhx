'use client'
import { useRouter } from "next/navigation"
export default function Login() {
    const router = useRouter()

    return (
        <main>
            <div className="m-5 grid grid-cols-3 gap-2">
                <div className="bg-gradient-to-br from-green-100 to-green-500 col-span-2 rounded-md p-4 h-screen flex flex-col justify-center items-center">
                 <p className="underline decoration-emerald-600 text-white text-5xl font-bold mb-4">Something here</p>

                    
                </div>

                <div className="bg-emerald-700 rounded-md p-4 h-screen flex flex-col justify-center items-center">
                    
                       
                    <p className="underline decoration-double decoration-emerald-900 text-white text-5xl font-bold mb-4">Spinich</p>
                    <button className="text-white shadow-lg shadow-black-700 font-bold rouded-lg p-5 m-auto bg-green-300 hover:bg-emerald-400 rounded-md p-4 outline outline-offset-2 outline-white transition ease-in-out delay-150 bg-emerald-500:-translate-y-1 hover:scale-110 hover:bg-green-700 duration-300" onClick ={() => router.push('/dashboard') }>Log in</button>

                </div> 

            </div> 

            

        </main>

    )
}