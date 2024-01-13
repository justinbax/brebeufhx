'use client'
import { useState } from 'react'
import { Api } from '../helpers/api'
import axios from 'axios'

export default function Dashboard() {
    const [arrOfRecipients, setArrOfRecipients]: [any, any] = useState([])
    function getDashboardData() {
        axios.get("http://localhost:3001/getListOfRecipients?own_email=cai.lucia04@gmail.com").then(
            (res) => {
                console.log(res.data.recipients);
                for (let i = 0; i < Object.keys(res.data.recipients).length; i++) {
                    axios.get(`http://localhost:3001/getRecipient?recipient=${res.data.recipients[i]}`).then(
                    
                        (res) => {
                            console.log(res.data)
                            setArrOfRecipients([...arrOfRecipients, res.data])
                            
                        }
                    )
                    
                }
                
            }
        )
        .finally(() => {
            console.log(arrOfRecipients)
        })
    }
    return (
        <main>
            <div className="grid grid-cols-2 gap-4 m-12">
                <div className="p-8 bg-slate-200 rounded-lg">
                    <h1 className="text-4xl">Welcome back, </h1>
                    <h1 className="text-4xl">"user whatever"</h1>

                </div>
                <div></div>
                <div className="bg-slate-100 col-span-2 p-10 rounded-lg place-conetent-center">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-2 m-4">
                    <div className="bg-slate-200 p-8 px-10  rounded-lg text-wrap">
                        <div className="py-2">
                        <div className="text-xl truncate" onClick={() =>     getDashboardData()
}>Chris Yang</div>
                        <div className="text-md truncate">XYang1876008@cdt.cadets.gc.ca</div>
                        </div>
                        <div className="py-2">
                        <div className="bg-red-500 text-lg pa-2 text-center">No Response</div>
                        <div className="text-md text-wrap pt-1">
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                        </div>
                        </div>

                    </div>
                    </div>

                </div>



            </div>


        </main>
    )
}