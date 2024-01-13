'use client'
import { useEffect, useState } from 'react'
import { Api } from '../helpers/api'
import axios from 'axios'

export default function Dashboard() {
    const [arrOfRecipients, setArrOfRecipients]: [any, any] = useState([])
    function getDashboardData() {
        axios.get("http://localhost:3001/getListOfRecipients?own_email=chrisyx511@gmail.com").then(
            (res) => {
                console.log(res.data.recipients);
                for (let i = 0; i < Object.keys(res.data.recipients).length; i++) {
                    axios.get(`http://localhost:3001/getRecipient?recipient=${res.data.recipients[i]}`).then(
                    
                        (res2) => {
                            console.log(res2.data)
                            let recipient = res2.data
                            recipient.email = res.data.recipients[i]
                            setArrOfRecipients((arrOfRecipients: any) => [...arrOfRecipients, recipient])
                            
                        }
                    )
                    
                }
                
            }
        )
        .finally(() => {
            console.log(arrOfRecipients)
        })
    }
    useEffect(() => {
        getDashboardData()
    }, [])
    return (
        <main>
            <div className="grid grid-cols-2 gap-4 m-12">
            <div className="p-8 bg-green-100 rounded-lg">
                    <h1 className="text-emerald-700 font-bold text-4xl">Welcome back, </h1>
                    <h1 className="text-emerald-900 font-semibold text-4xl">chrisyx511@gmail.com</h1>

                </div>                <div></div>
                <div className="bg-emerald-400 col-span-2 p-10 rounded-lg place-conetent-center">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-2 m-4">

                    {
                        Array.from({length: arrOfRecipients.length}, (_, i) => {
                            return (
                            <div key={i} className="bg-green-200 p-8 px-10 rounded-lg text-wrap">
                            <div className="py-2">
                            <div className="text-xl truncate">{arrOfRecipients[i].first_name + ' ' + arrOfRecipients[i].last_name} </div>
                            <div className="text-md truncate">{arrOfRecipients[i].email}</div>
                            </div>
                            <div className="py-2">
                            <Status code={arrOfRecipients[i].status}></Status>

                            <div className="text-md text-wrap pt-1">
                                {arrOfRecipients[i].desc}
                            </div>
                            </div>
    
                        </div>
    
                        )})
                    }

                    </div>

                </div>



            </div>


        </main>
    )

    function Status({code}: any) {
        switch (code) {
            case "NR": 
            return (
                <div className="bg-slate-500 text-lg pa-2 text-center">
                    No Reply
                </div>
            )
        case "RP":
            return (
                <div className="bg-green-500 text-lg pa-2 text-center">
                Reply Positive
                </div>
            )
        case "RN":
            return (                
            <div className="bg-red-500 text-lg pa-2 text-center">
                    Reply Negative
            </div>
            )
        default:
            return ""        }
    }
}