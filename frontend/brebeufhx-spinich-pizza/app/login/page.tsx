'use client'
import { useRouter } from "next/navigation"
export default function Login() {
    const router = useRouter()

    return (
        <main>
            <div className="m-5 grid grid-cols-3 gap-2">
                <div className="bg-gradient-to-br from-green-100 to-green-500 col-span-2 rounded-md p-4 h-screen">
                    
                </div>

                <div className="bg-emerald-700 rounded-md p-4 h-screen flex">
                    <button className="rouded-lg p-5 m-auto bg-green-300 hover:bg-green-400 rounded-md p-4" onClick ={() => router.push('/dashboard') }>Log in</button>
                </div> 
            </div> 

            

        </main>

    )
}